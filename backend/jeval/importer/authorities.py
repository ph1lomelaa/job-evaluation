"""Шаблон 'Полномочия' по умолчанию — когда документ не описывает явно,
что роль решает сама / согласует / рекомендует, но Gate 0 требует этот блок
(раздел 3.2: «нет понимания — нет оценки»).

Это НЕ извлечение фактов из текста и не вызов LLM — детерминированное
допущение по организационной иерархии (роль решает в своей зоне, согласует
с непосредственным руководителем). Каждый сгенерированный пункт помечен
AUTHORITY_ASSUMPTION_MARKER; jeval/qc.py::run_qc обязан найти этот маркер
и вернуть FAIL (см. authorities_assumed), чтобы предположение не прошло
как подтверждённый факт — только явный опт-ин (см. import_router), не
автоматическое поведение.
"""

from __future__ import annotations

from typing import Optional

from ..domain.models import ApprovalItem, Authorities, JobDossier
from ..qc import AUTHORITY_ASSUMPTION_MARKER


def infer_default_authorities(dossier: JobDossier) -> Optional[Authorities]:
    """Шаблон полномочий, если документ их не описывает и есть руководитель,
    относительно которого можно сформулировать допущение. Не перетирает уже
    найденные в документе полномочия — вызывающий код должен сам решить,
    нужно ли это (см. fill_default_authorities в import_document)."""
    a = dossier.authorities
    if a.decides_alone or a.requires_approval or a.recommends:
        return None
    manager = dossier.reporting.manager
    if not manager:
        return None
    return Authorities(
        decides_alone=[
            f"{AUTHORITY_ASSUMPTION_MARKER} Операционные решения в рамках зоны "
            "ответственности подразделения, без согласования с подчинёнными"
        ],
        requires_approval=[
            ApprovalItem(
                item=f"{AUTHORITY_ASSUMPTION_MARKER} Решения за пределами полномочий "
                "подразделения",
                approver=manager,
            )
        ],
    )


def default_authorities_note(manager: str) -> str:
    return (
        f"{AUTHORITY_ASSUMPTION_MARKER} Раздел «Полномочия» не найден в документе. "
        f"Заполнен по умолчанию исходя из организационной иерархии (подчиняется: "
        f"{manager}) — обязательно проверьте и замените реальными фактами перед "
        "оценкой."
    )
