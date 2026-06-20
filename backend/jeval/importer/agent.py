"""LLM-экстрактор JE-досье из текста документа.

Агент используется только для заполнения черновика. Он не оценивает факторы и
не должен придумывать отсутствующие данные.
"""

from __future__ import annotations

import json
import re
from typing import Optional

from pydantic import BaseModel, Field, field_validator

from ..config import get_settings
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


class DossierDraftOutput(BaseModel):
    name: str = "Импортированная должность"
    dzo: Optional[str] = None
    department: Optional[str] = None
    function: Optional[str] = None
    purpose: Optional[str] = None
    key_results: list[str] = Field(default_factory=list)
    responsibilities: list[str] = Field(default_factory=list)
    kpis: list[str] = Field(default_factory=list)
    manager: Optional[str] = None
    subordinates: list[str] = Field(default_factory=list)
    decides_alone: list[str] = Field(default_factory=list)
    requires_approval: list[str] = Field(default_factory=list)
    recommends: list[str] = Field(default_factory=list)
    limits: list[str] = Field(default_factory=list)
    annual_opex: Optional[float] = None
    annual_capex: Optional[float] = None
    annual_revenue: Optional[float] = None
    function_budget: Optional[float] = None
    project_portfolio: Optional[float] = None
    headcount: Optional[int] = None
    assets: Optional[str] = None
    scope_source: Optional[str] = None
    stakeholders: list[str] = Field(default_factory=list)
    organizational_context: Optional[str] = None
    anchor_roles: list[str] = Field(default_factory=list)
    problem_cases: list[str] = Field(default_factory=list)
    documents: list[str] = Field(default_factory=list)
    confirmed_by: Optional[str] = None
    extracted_fields: list[str] = Field(default_factory=list)
    missing_fields: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    confidence: Confidence = Confidence.LOW

    @field_validator("name", mode="before")
    @classmethod
    def _coerce_name(cls, value: object) -> str:
        if value is None or value == []:
            return "Импортированная должность"
        if isinstance(value, str):
            stripped = value.strip()
            return stripped or "Импортированная должность"
        return str(value).strip() or "Импортированная должность"

    @field_validator(
        "key_results",
        "responsibilities",
        "kpis",
        "subordinates",
        "decides_alone",
        "requires_approval",
        "recommends",
        "limits",
        "stakeholders",
        "anchor_roles",
        "problem_cases",
        "documents",
        "extracted_fields",
        "missing_fields",
        "notes",
        mode="before",
    )
    @classmethod
    def _coerce_list(cls, value: object) -> list[str]:
        if value is None:
            return []
        if isinstance(value, list):
            return [str(item).strip() for item in value if str(item).strip()]
        if isinstance(value, str):
            stripped = value.strip()
            return [stripped] if stripped else []
        return []

    @field_validator(
        "annual_opex",
        "annual_capex",
        "annual_revenue",
        "function_budget",
        "project_portfolio",
        mode="before",
    )
    @classmethod
    def _coerce_optional_number(cls, value: object) -> Optional[float]:
        if value is None or value == []:
            return None
        if isinstance(value, (int, float)):
            return float(value)
        if isinstance(value, str):
            cleaned = value.strip().replace(" ", "").replace(",", ".")
            if not cleaned:
                return None
            try:
                return float(cleaned)
            except ValueError:
                return None
        return None

    @field_validator("headcount", mode="before")
    @classmethod
    def _coerce_optional_int(cls, value: object) -> Optional[int]:
        if value is None or value == []:
            return None
        if isinstance(value, int):
            return value
        if isinstance(value, float) and value.is_integer():
            return int(value)
        if isinstance(value, str):
            cleaned = value.strip().replace(" ", "")
            if not cleaned:
                return None
            try:
                return int(float(cleaned))
            except ValueError:
                return None
        return None

    @field_validator(
        "assets",
        "scope_source",
        "manager",
        "dzo",
        "department",
        "function",
        "purpose",
        "organizational_context",
        "confirmed_by",
        mode="before",
    )
    @classmethod
    def _coerce_optional_str(cls, value: object) -> Optional[str]:
        if value is None or value == []:
            return None
        if isinstance(value, str):
            stripped = value.strip()
            return stripped or None
        return str(value).strip() or None


_SYSTEM = """
Ты извлекаешь JE-досье из текста описания должности.

КРИТИЧЕСКОЕ ПРАВИЛО: НИКОГДА НЕ ПРИДУМЫВАЙ ИНФОРМАЦИЮ.
Если поле прямо не найдено в документе, верни null для строки/числа или [] для списка.
Не выводи бюджет, полномочия, KPI, подчиненных, функцию или масштаб из здравого смысла.
Не оценивай должность по Hay, не выбирай уровни факторов, не присваивай баллы и грейд.

Верни только валидный JSON по схеме. Все элементы списков должны быть короткими фактами из документа.
"""

_USER_TEMPLATE = """
Извлеки черновик JE-досье из документа.

JSON-поля:
name, dzo, department, function, purpose, key_results, responsibilities, kpis,
manager, subordinates, decides_alone, requires_approval, recommends, limits,
annual_opex, annual_capex, annual_revenue, function_budget, project_portfolio,
headcount, assets, scope_source, stakeholders, organizational_context,
anchor_roles, problem_cases, documents, confirmed_by, extracted_fields,
missing_fields, notes, confidence.

Правила:
- missing_fields заполни названиями важных полей, которых нет в тексте.
- extracted_fields заполни только полями, которые реально найдены.
- notes используй для предупреждений о неоднозначности извлечения.
- confidence: high только если большинство ключевых блоков явно найдены, иначе medium/low.
- subordinates — только список названий подчиненных должностей/групп. Если в документе есть только число подчиненных, запиши его в headcount, а subordinates оставь [].
- Все поля со списками всегда возвращай как массив JSON, даже если данных нет: [].

Текст документа:
{text}
"""

_JSON_BLOCK = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


class DossierExtractionAgent:
    def __init__(self, provider: Optional[str] = None) -> None:
        settings = get_settings()
        self._provider = provider or settings.jeval_agent_provider
        self._settings = settings

    def extract(
        self,
        text: str,
        *,
        source_filename: Optional[str] = None,
        source_mime_type: Optional[str] = None,
        source_size_bytes: Optional[int] = None,
        source_sha256: Optional[str] = None,
        source_blocks: Optional[list[ParsedBlock]] = None,
        max_tokens: int = 4096,
    ) -> DossierImportResult:
        if self._provider == "groq":
            out = self._extract_groq(text, max_tokens=max_tokens)
        elif self._provider == "anthropic":
            out = self._extract_anthropic(text, max_tokens=max_tokens)
        else:
            raise RuntimeError("ИИ-извлечение недоступно для provider=fake")
        return _to_import_result(
            out,
            text,
            source_filename=source_filename,
            source_mime_type=source_mime_type,
            source_size_bytes=source_size_bytes,
            source_sha256=source_sha256,
            source_blocks=source_blocks or [],
            method=f"ai_{self._provider}",
        )

    def _extract_groq(self, text: str, *, max_tokens: int) -> DossierDraftOutput:
        if not self._settings.groq_api_key:
            raise RuntimeError("GROQ_API_KEY не задан")
        from groq import Groq

        client = Groq(api_key=self._settings.groq_api_key)
        response = client.chat.completions.create(
            model=self._settings.groq_model,
            temperature=0,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": _SYSTEM},
                {"role": "user", "content": _USER_TEMPLATE.format(text=text[:45000])},
            ],
        )
        raw = response.choices[0].message.content or ""
        return DossierDraftOutput.model_validate(_extract_json(raw))

    def _extract_anthropic(self, text: str, *, max_tokens: int) -> DossierDraftOutput:
        if not self._settings.anthropic_api_key:
            raise RuntimeError("ANTHROPIC_API_KEY не задан")
        import anthropic

        client = anthropic.Anthropic(api_key=self._settings.anthropic_api_key)
        response = client.messages.create(
            model=self._settings.jeval_model,
            max_tokens=max_tokens,
            temperature=0,
            system=_SYSTEM,
            messages=[{"role": "user", "content": _USER_TEMPLATE.format(text=text[:45000])}],
        )
        raw = "\n".join(getattr(block, "text", "") for block in response.content)
        return DossierDraftOutput.model_validate(_extract_json(raw))


def _extract_json(text: str) -> dict:
    match = _JSON_BLOCK.search(text)
    raw = match.group(1) if match else text.strip()
    raw = re.sub(r",\s*([}\]])", r"\1", raw)
    return json.loads(raw)


def _to_import_result(
    out: DossierDraftOutput,
    raw_text: str,
    *,
    source_filename: Optional[str],
    source_mime_type: Optional[str],
    source_size_bytes: Optional[int],
    source_sha256: Optional[str],
    source_blocks: list[ParsedBlock],
    method: str,
) -> DossierImportResult:
    notes = [
        "Черновик заполнен ИИ из текста документа. Проверьте все поля перед Gate 0.",
        "ИИ обязан оставлять отсутствующие поля пустыми; проверьте missing_fields.",
        *out.notes,
    ]
    documents = out.documents[:]
    if source_filename and source_filename not in documents:
        documents.append(source_filename)

    dossier = JobDossier(
        name=out.name or "Импортированная должность",
        dzo=out.dzo,
        department=out.department,
        function=out.function,
        purpose=out.purpose,
        key_results=out.key_results,
        responsibilities=out.responsibilities,
        kpis=out.kpis,
        reporting=Reporting(
            manager=out.manager,
            subordinates=out.subordinates,
            matrix_links=[],
        ),
        authorities=Authorities(
            decides_alone=out.decides_alone,
            recommends=out.recommends,
        ),
        limits=out.limits,
        scope=Scope(
            annual_opex=out.annual_opex,
            annual_capex=out.annual_capex,
            annual_revenue=out.annual_revenue,
            function_budget=out.function_budget,
            project_portfolio=out.project_portfolio,
            headcount=out.headcount,
            assets=out.assets,
            source=out.scope_source,
        ),
        stakeholders=out.stakeholders,
        organizational_context=out.organizational_context,
        anchor_roles=out.anchor_roles,
        problem_cases=out.problem_cases,
        documents=documents,
        confirmed_by=out.confirmed_by,
        review_status=DossierReviewStatus.DRAFT_IMPORTED,
        import_metadata=ImportMetadata(
            source_filename=source_filename,
            source_type="docx",
            source_mime_type=source_mime_type,
            source_size_bytes=source_size_bytes,
            source_sha256=source_sha256,
            extraction_method=method,
            confidence=out.confidence,
            notes=notes,
            missing_fields=out.missing_fields,
            field_sources=_ai_field_sources(source_blocks),
            raw_text_preview=raw_text[:2000],
        ),
    )
    return DossierImportResult(
        position=dossier,
        raw_text=raw_text,
        extracted_fields=out.extracted_fields,
        missing_fields=out.missing_fields,
        notes=notes,
    )


def _ai_field_sources(source_blocks: list[ParsedBlock]) -> dict[str, list[str]]:
    provenance: dict[str, list[str]] = {"ai_import": []}
    for block in source_blocks[:20]:
        provenance["ai_import"].append(_describe_block(block))
    return provenance


def _describe_block(block: ParsedBlock) -> str:
    parts = [block.kind]
    if block.paragraph_index is not None:
        parts.append(f"p{block.paragraph_index}")
    if block.table_index is not None:
        parts.append(f"t{block.table_index}")
    if block.row_index is not None:
        parts.append(f"r{block.row_index}")
    if block.cell_index is not None:
        parts.append(f"c{block.cell_index}")
    return f"{'/'.join(parts)}: {block.text[:240]}"
