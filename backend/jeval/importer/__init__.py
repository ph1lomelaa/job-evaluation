"""Импорт JE-досье из внешних документов."""

from .docx import ParsedDocument, extract_docx_text
from .extractor import build_dossier_from_text

__all__ = ["ParsedDocument", "extract_docx_text", "build_dossier_from_text"]
