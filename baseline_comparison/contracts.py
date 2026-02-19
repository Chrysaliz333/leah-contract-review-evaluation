"""Extract text from .docx contract files using python-docx."""

from pathlib import Path

from docx import Document


def extract_text(docx_path: Path) -> str:
    """Extract full text from a .docx file, joining paragraphs with newlines.

    Args:
        docx_path: Path to the .docx file.

    Returns:
        The full text content of the document.

    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file is empty or unreadable.
    """
    if not docx_path.exists():
        raise FileNotFoundError(f"Contract not found: {docx_path}")

    doc = Document(str(docx_path))
    paragraphs = [p.text for p in doc.paragraphs if p.text.strip()]

    if not paragraphs:
        raise ValueError(f"No text extracted from: {docx_path}")

    return "\n\n".join(paragraphs)
