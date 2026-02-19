"""API wrappers for OpenAI and Anthropic with retry/backoff."""

import time
import logging
from dataclasses import dataclass

import openai
import anthropic

logger = logging.getLogger(__name__)

MAX_RETRIES = 3
INITIAL_BACKOFF = 2.0  # seconds


@dataclass
class LLMResponse:
    """Standardised response from any LLM provider."""

    text: str
    model: str
    input_tokens: int
    output_tokens: int
    latency_seconds: float


def _retry_with_backoff(fn, *, max_retries: int = MAX_RETRIES):
    """Call fn() with exponential backoff on rate-limit or transient errors."""
    for attempt in range(max_retries + 1):
        try:
            return fn()
        except (
            openai.RateLimitError,
            openai.APITimeoutError,
            openai.InternalServerError,
            anthropic.RateLimitError,
            anthropic.APITimeoutError,
            anthropic.InternalServerError,
        ) as exc:
            if attempt == max_retries:
                raise
            wait = INITIAL_BACKOFF * (2 ** attempt)
            logger.warning(
                "Retryable error (attempt %d/%d), waiting %.1fs: %s",
                attempt + 1, max_retries, wait, exc,
            )
            time.sleep(wait)


def call_openai(
    prompt: str,
    *,
    model: str,
    api_key: str,
    max_tokens: int = 16_000,
) -> LLMResponse:
    """Send a single-turn prompt to an OpenAI model.

    Args:
        prompt: The full user message.
        model: OpenAI model ID (e.g. "o3", "gpt-4.1").
        api_key: OpenAI API key.
        max_tokens: Maximum response tokens.

    Returns:
        LLMResponse with the model's text and usage metadata.
    """
    client = openai.OpenAI(api_key=api_key)

    # o-series models (o1, o3, etc.) require max_completion_tokens
    _is_o_series = model.startswith("o")
    token_param = "max_completion_tokens" if _is_o_series else "max_tokens"

    def _call():
        return client.chat.completions.create(
            model=model,
            messages=[{"role": "user", "content": prompt}],
            **{token_param: max_tokens},
        )

    t0 = time.monotonic()
    try:
        response = _retry_with_backoff(_call)
    except openai.AuthenticationError as exc:
        raise RuntimeError(
            f"OpenAI authentication failed for model {model}. "
            f"Check your API key has the 'model.request' scope: {exc}"
        ) from exc
    latency = time.monotonic() - t0

    choice = response.choices[0]
    usage = response.usage

    return LLMResponse(
        text=choice.message.content or "",
        model=response.model,
        input_tokens=usage.prompt_tokens if usage else 0,
        output_tokens=usage.completion_tokens if usage else 0,
        latency_seconds=round(latency, 2),
    )


def call_anthropic(
    prompt: str,
    *,
    system: str = "",
    model: str,
    api_key: str,
    max_tokens: int = 8_000,
) -> LLMResponse:
    """Send a single-turn prompt to an Anthropic model.

    Args:
        prompt: The user message content.
        system: Optional system prompt.
        model: Anthropic model ID.
        api_key: Anthropic API key.
        max_tokens: Maximum response tokens.

    Returns:
        LLMResponse with the model's text and usage metadata.
    """
    client = anthropic.Anthropic(api_key=api_key)

    def _call():
        kwargs = dict(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        if system:
            kwargs["system"] = system
        return client.messages.create(**kwargs)

    t0 = time.monotonic()
    response = _retry_with_backoff(_call)
    latency = time.monotonic() - t0

    text = ""
    for block in response.content:
        if block.type == "text":
            text += block.text

    return LLMResponse(
        text=text,
        model=response.model,
        input_tokens=response.usage.input_tokens,
        output_tokens=response.usage.output_tokens,
        latency_seconds=round(latency, 2),
    )
