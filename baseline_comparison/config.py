"""Constants, paths, and model configuration for baseline comparison."""

from pathlib import Path

# --- Directories ---

PROJECT_ROOT = Path(__file__).resolve().parent.parent
BASELINE_DIR = Path(__file__).resolve().parent

CONTRACTS_DIR = PROJECT_ROOT / "freeform" / "contracts"
GT_DIR = PROJECT_ROOT / "freeform" / "ground_truth"
FREEFORM_CONFIG = PROJECT_ROOT / "framework" / "config" / "freeform.json"

RAW_RESPONSES_DIR = BASELINE_DIR / "raw_responses"
RESULTS_DIR = BASELINE_DIR / "results"
REPORTS_DIR = BASELINE_DIR / "reports"

ENV_FILE = Path("/Users/liz/Work/.env")

# --- Contract mapping: short name → docx filename ---

CONTRACT_FILES: dict[str, str] = {
    "consulting": "Consulting_TechAdvisors_Beta.docx",
    "dpa": "DPA_DataServices.docx",
    "distribution": "Distribution_GlobalPartners.docx",
    "jv": "JV_MOU_InnovateTech.docx",
    "license": "License_IPHoldings.docx",
    "partnership": "Partnership_VentureAlliance.docx",
    "reseller": "Reseller_TechDistributors.docx",
    "services": "Services_DigitalAgency.docx",
    "sla": "SLA_CloudServices_Alpha.docx",
    "supply": "Supply_ManufacturingCo.docx",
}

ALL_CONTRACTS = list(CONTRACT_FILES.keys())

# --- Model configuration ---

MODELS: dict[str, dict] = {
    "o3": {
        "provider": "openai",
        "api_model": "o3",
        "display_name": "OpenAI o3",
    },
    "gpt41": {
        "provider": "openai",
        "api_model": "gpt-4.1",
        "display_name": "GPT-4.1",
    },
    "haiku35": {
        "provider": "anthropic",
        "api_model": "claude-3-5-haiku-20241022",
        "display_name": "Claude 3.5 Haiku",
        "max_tokens": 8192,
    },
    "sonnet4": {
        "provider": "anthropic",
        "api_model": "claude-sonnet-4-20250514",
        "display_name": "Claude Sonnet 4",
        "max_tokens": 16_000,
    },
}

ALL_MODELS = list(MODELS.keys())

# --- Evaluator model ---

EVALUATOR_MODEL = "claude-sonnet-4-20250514"
EVALUATOR_PROVIDER = "anthropic"

# --- Scoring config (mirrors framework/config/freeform.json) ---

DETECTION_POINTS: dict[str, dict[str, float]] = {
    "T1": {"Y": 8, "P": 4, "N": 0, "NMI": 0},
    "T2": {"Y": 5, "P": 2.5, "N": 0, "NMI": 0},
    "T3": {"Y": 1, "P": 0.5, "N": 0, "NMI": 0},
}

# --- Prompt ---

RAW_REVIEW_PROMPT = "Review this contract"
