"""Сборка черновика `JobDossier` из текста документа.

Этот слой намеренно консервативный: он заполняет только поля, найденные в
документе по явным заголовкам/меткам. Если поле не найдено, оно остается
`None` или пустым списком.
"""

from __future__ import annotations

import re
from typing import Optional

from ..domain.enums import Confidence, DossierReviewStatus
from ..domain.models import (
    Authorities,
    DossierImportResult,
    ImportMetadata,
    JobDossier,
    Reporting,
    Scope,
)
from .docx import ParsedBlock

# См. agent.py::_RAW_TEXT_PREVIEW_LIMIT — тот же лимит, чтобы оба пути импорта
# (ИИ и эвристика) не обрезали документ до критичных для Know-How разделов.
_RAW_TEXT_PREVIEW_LIMIT = 12000


_SECTION_TITLES = (
    "Общая информация",
    "Цель существования должности",
    "Цель должности",
    "Количественные показатели масштаба деятельности должности",
    "Количественные показатели",
    "Органиграмма",
    "Навыки, знания и опыт",
    "Основные области ответственности",
    "Основные показатели эффективности работы",
    "Основные показатели эффективности",
    "Дополнительная информация о должности",
)

_REQUIRED_FIELDS = (
    "name",
    "dzo",
    "department",
    "reporting.manager",
    "purpose",
    "key_results",
    "responsibilities",
    "kpis",
    "authorities",
    "scope",
    "organizational_context",
)


def build_dossier_from_text(
    text: str,
    *,
    source_filename: Optional[str] = None,
    extraction_method: str = "heuristic_docx",
    source_mime_type: Optional[str] = None,
    source_size_bytes: Optional[int] = None,
    source_sha256: Optional[str] = None,
    source_blocks: Optional[list[ParsedBlock]] = None,
) -> DossierImportResult:
    """Построить черновик из текста.

    Функция не выводит отсутствующие данные из контекста. Например, если в
    документе нет бюджета, `scope.annual_opex` останется `None`.
    """
    normalized = _normalize(text)
    sections = _sections(normalized)
    field_sources = _heuristic_field_sources(normalized, sections, source_blocks or [])

    name = _first_match(
        normalized,
        (
            r"Название должности\s*:?\s*\|?\s*(.+)",
            r"Описание должности\s*\n(.+)",
        ),
    ) or "Импортированная должность"
    dzo = _first_match(normalized, (r"Название Компании\s*:?\s*\|?\s*(.+)",))
    department = _first_match(normalized, (r"Подразделение\s*:?\s*\|?\s*(.+)",))
    manager = _first_match(normalized, (r"Подчиняется\s*:?\s*\|?\s*(.+)",))

    purpose = _section_payload(
        sections,
        "Цель существования должности",
        "Цель должности",
        strip_intro=("Цель должности", "Цель существования должности"),
    )
    responsibilities = _list_from_section(
        sections,
        "Основные области ответственности",
        drop_prefix="Основные области ответственности",
    )
    key_results = _key_results_from_items(responsibilities)
    kpis = _list_from_section(
        sections,
        "Основные показатели эффективности работы",
        "Основные показатели эффективности",
        drop_prefix="Основные показатели эффективности",
        skip_contains=("критерии, связанные с областями ответственности", "они выражаются"),
    )
    skills = _section_payload(
        sections,
        "Навыки, знания и опыт",
        strip_intro=("Навыки, знания и опыт",),
        drop_contains=("необходимый минимальный уровень образования",),
    )
    extra = _section_payload(
        sections,
        "Дополнительная информация о должности",
        strip_intro=("Дополнительная информация о должности",),
    )
    scope_text = _section_payload(
        sections,
        "Количественные показатели масштаба деятельности должности",
        "Количественные показатели",
    )
    headcount = _extract_headcount(scope_text)

    extracted_fields = _present_fields(
        {
            "name": name if name != "Импортированная должность" else None,
            "dzo": dzo,
            "department": department,
            "reporting.manager": manager,
            "purpose": purpose,
            "key_results": key_results,
            "responsibilities": responsibilities,
            "kpis": kpis,
            "authorities": [],
            "scope": headcount or scope_text,
            "organizational_context": extra,
        }
    )
    missing = [field for field in _REQUIRED_FIELDS if field not in extracted_fields]
    notes = [
        "Черновик импортирован из документа. Проверьте все поля перед Gate 0.",
        "Поля, не найденные явно в документе, оставлены пустыми.",
    ]
    if skills:
        notes.append("Раздел 'Навыки, знания и опыт' сохранен в документах/контексте, но не превращен в уровни факторов.")

    dossier = JobDossier(
        name=_clean_value(name),
        dzo=_clean_optional(dzo),
        department=_clean_optional(department),
        purpose=_clean_optional(purpose),
        key_results=key_results,
        responsibilities=responsibilities,
        kpis=kpis,
        reporting=Reporting(manager=_clean_optional(manager), subordinates=[], matrix_links=[]),
        authorities=Authorities(),
        scope=Scope(headcount=headcount),
        organizational_context=_join_optional(extra, skills),
        documents=[source_filename] if source_filename else [],
        review_status=DossierReviewStatus.DRAFT_IMPORTED,
        import_metadata=ImportMetadata(
            source_filename=source_filename,
            source_type="docx",
            source_mime_type=source_mime_type,
            source_size_bytes=source_size_bytes,
            source_sha256=source_sha256,
            extraction_method=extraction_method,
            confidence=Confidence.MEDIUM if len(extracted_fields) >= 5 else Confidence.LOW,
            notes=notes,
            missing_fields=missing,
            field_sources=field_sources,
            raw_text_preview=normalized[:_RAW_TEXT_PREVIEW_LIMIT],
        ),
    )

    return DossierImportResult(
        position=dossier,
        raw_text=normalized,
        extracted_fields=extracted_fields,
        missing_fields=missing,
        notes=notes,
    )


def _normalize(text: str) -> str:
    lines = [" ".join(line.strip().split()) for line in text.replace("\r", "\n").split("\n")]
    cleaned = [line for line in lines if line]
    return "\n".join(cleaned)


def _sections(text: str) -> dict[str, str]:
    matches: list[tuple[int, str]] = []
    for title in _SECTION_TITLES:
        for m in re.finditer(rf"(?im)^{re.escape(title)}\s*$", text):
            matches.append((m.start(), title))
    matches.sort()
    result: dict[str, str] = {}
    for idx, (start, title) in enumerate(matches):
        end = matches[idx + 1][0] if idx + 1 < len(matches) else len(text)
        payload = text[start + len(title):end].strip()
        result.setdefault(title, payload)
    return result


def _first_match(text: str, patterns: tuple[str, ...]) -> Optional[str]:
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            value = _clean_value(match.group(1))
            if value:
                return value
    return None


def _section_payload(
    sections: dict[str, str],
    *titles: str,
    strip_intro: tuple[str, ...] = (),
    drop_contains: tuple[str, ...] = (),
) -> Optional[str]:
    for title in titles:
        payload = sections.get(title)
        if not payload:
            continue
        value = payload.replace("--- TABLE ---", "").replace("--- END TABLE ---", "").strip()
        for intro in strip_intro:
            value = re.sub(
                rf"^{re.escape(intro)}[^\n]*(?:основная цель существования|обобщенный ожидаемый вклад)[^\n]*\n?",
                "",
                value,
                flags=re.IGNORECASE,
            ).strip()
            value = re.sub(
                rf"^{re.escape(intro)}\s*[–-][^\n]*?(?=\n|[А-ЯA-Z][а-яa-z]+\s)",
                "",
                value,
                flags=re.IGNORECASE,
            ).strip()
            value = re.sub(rf"^{re.escape(intro)}[^.\n]*\.?", "", value, flags=re.IGNORECASE).strip()
        for marker in drop_contains:
            value = "\n".join(
                line for line in value.split("\n") if marker.lower() not in line.lower()
            )
        value = _clean_value(value)
        if value:
            return value
    return None


def _list_from_section(
    sections: dict[str, str],
    *titles: str,
    drop_prefix: Optional[str] = None,
    skip_contains: tuple[str, ...] = (),
) -> list[str]:
    payload = _section_payload(sections, *titles)
    if not payload:
        return []
    if drop_prefix:
        payload = re.sub(rf"^{re.escape(drop_prefix)}[^.\n]*\.?", "", payload, flags=re.IGNORECASE).strip()
    items = re.split(r"(?:\n|;)+|(?=\b\d+(?:\.\d+)*\.\s+)", payload)
    result: list[str] = []
    for item in items:
        item = _clean_value(item)
        if not item or len(item) < 3:
            continue
        if item.lower() in {"table", "end table"}:
            continue
        if any(marker.lower() in item.lower() for marker in skip_contains):
            continue
        result.append(item)
    return _dedupe(result)


def _heuristic_field_sources(
    text: str,
    sections: dict[str, str],
    blocks: list[ParsedBlock],
) -> dict[str, list[str]]:
    """Provenance-карта для контекста и аудита импорта."""
    sources: dict[str, list[str]] = {}

    def add(field: str, value: Optional[str]) -> None:
        if not value:
            return
        snippet = " ".join(value.split()).strip()
        if not snippet:
            return
        bucket = sources.setdefault(field, [])
        if snippet[:240] not in bucket:
            bucket.append(snippet[:240])

    def add_block(field: str, needle: str) -> None:
        block = _first_block(blocks, needle)
        if block:
            add(field, _block_summary(block))

    def add_window(field: str, needle: str, size: int = 4) -> None:
        window = _block_window(blocks, needle, size=size)
        if window:
            add(field, " || ".join(_block_summary(block) for block in window))

    add_block("name", "Название должности")
    add_block("name", "Описание должности")
    add_block("dzo", "Название Компании")
    add_block("department", "Подразделение")
    add_block("reporting.manager", "Подчиняется")
    add_window("purpose", "Цель существования должности")
    add_window("purpose", "Цель должности")
    add_window("key_results", "Основные области ответственности")
    add_window("responsibilities", "Основные области ответственности")
    add_window("kpis", "Основные показатели эффективности")
    add_window("scope", "Количественные показатели масштаба деятельности должности")
    add_window("scope", "Количественные показатели")
    add_window("organizational_context", "Дополнительная информация о должности")
    add_window("skills", "Навыки, знания и опыт")
    return sources


def _first_block(blocks: list[ParsedBlock], needle: str) -> Optional[ParsedBlock]:
    index = _block_index(blocks, needle)
    return blocks[index] if index is not None else None


def _block_index(blocks: list[ParsedBlock], needle: str) -> Optional[int]:
    needle_norm = needle.casefold()
    for index, block in enumerate(blocks):
        if needle_norm in block.text.casefold():
            return index
    return None


def _block_window(blocks: list[ParsedBlock], needle: str, size: int = 4) -> list[ParsedBlock]:
    start = _block_index(blocks, needle)
    if start is None:
        return []
    window: list[ParsedBlock] = []
    for block in blocks[start:start + size]:
        window.append(block)
        if len(window) >= size:
            break
    return window


def _block_summary(block: ParsedBlock) -> str:
    location: list[str] = [block.kind]
    if block.paragraph_index is not None:
        location.append(f"p{block.paragraph_index}")
    if block.table_index is not None:
        location.append(f"t{block.table_index}")
    if block.row_index is not None:
        location.append(f"r{block.row_index}")
    if block.cell_index is not None:
        location.append(f"c{block.cell_index}")
    return f"{'/'.join(location)}: {block.text[:240]}"


def _extract_headcount(text: Optional[str]) -> Optional[int]:
    if not text:
        return None
    patterns = (
        r"Количество непосредственных подчиненных\s*[–-]\s*(\d+)",
        r"подчиненных\s*[–-]\s*(\d+)",
        r"численность[^0-9]{0,40}(\d+)",
    )
    for pattern in patterns:
        match = re.search(pattern, text, flags=re.IGNORECASE)
        if match:
            return int(match.group(1))
    return None


def _key_results_from_items(items: list[str]) -> list[str]:
    """Верхнеуровневые пункты ответственности как явные конечные результаты."""
    results: list[str] = []
    for item in items:
        if re.match(r"^\d+\.\s+(?!\d)", item):
            cleaned = re.sub(r"^\d+\.\s+", "", item).strip()
            if cleaned and cleaned[0].isupper() and len(cleaned) <= 160:
                results.append(cleaned)
    return _dedupe(results)


def _present_fields(values: dict[str, object]) -> list[str]:
    present: list[str] = []
    for key, value in values.items():
        if isinstance(value, list):
            if value:
                present.append(key)
        elif value:
            present.append(key)
    return present


def _clean_optional(value: Optional[str]) -> Optional[str]:
    cleaned = _clean_value(value or "")
    return cleaned or None


def _clean_value(value: str) -> str:
    value = value.replace("--- TABLE ---", "").replace("--- END TABLE ---", "")
    value = re.sub(r"^Критерии эффективности и результативности:\s*", "", value, flags=re.IGNORECASE)
    value = re.sub(r"\s*\|\s*", " ", value)
    value = re.sub(r"\s{2,}", " ", value)
    return value.strip(" :-\n\t")


def _join_optional(*values: Optional[str]) -> Optional[str]:
    parts = [_clean_value(v) for v in values if v and _clean_value(v)]
    return "\n\n".join(parts) if parts else None


def _dedupe(items: list[str]) -> list[str]:
    seen: set[str] = set()
    result: list[str] = []
    for item in items:
        key = item.lower()
        if key in seen:
            continue
        seen.add(key)
        result.append(item)
    return result
