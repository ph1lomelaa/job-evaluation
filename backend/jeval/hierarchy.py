"""Проверка иерархии (раздел 9.5): сравнение с якорями и руководителем.

Работает по данным, уже накопленным в системе: ищет среди оценённых должностей
якоря (по названию) и непосредственного руководителя, затем проверяет:
  * подчинённый не выше руководителя по управленческому уровню Know-How;
  * дистанция в грейдах до якоря соответствует 15%-правилу (3+ шага — разрыв);
  * должности одного профиля похожи по природе работы (разные профили — флаг).
"""

from __future__ import annotations

from .domain.enums import ManagerialKnowHow, QCSeverity, QCStatus
from .domain.models import Evaluation, FactorSelections, JobDossier, QCFlag, ScoreResult
from .scoring.grades import steps_15pct

# Порядок управленческих уровней для сравнения «руководитель ≥ подчинённый».
_MGMT_ORDER: dict[str, int] = {m.value: i for i, m in enumerate(ManagerialKnowHow)}
_LETTER_ORDER = {v: i for i, v in enumerate("ABCDEFGH")}
_COMM_ORDER = {"1": 0, "2": 1, "3": 2}
_COMPLEXITY_ORDER = {str(i): i for i in range(1, 6)}
_MAGNITUDE_ORDER = {"N": 0, "1": 1, "2": 2, "3": 3, "4": 4}
_IMPACT_ORDER = {"R": 0, "C": 1, "S": 2, "P": 3}


def _norm(s: str) -> str:
    return " ".join(s.lower().split())


def _find_peer(
    name: str, peers: list[tuple[JobDossier, Evaluation]]
) -> tuple[JobDossier, Evaluation] | None:
    """Найти оценённую должность по названию (вхождение в любую сторону)."""
    target = _norm(name)
    if not target:
        return None
    for dossier, evaluation in peers:
        peer_name = _norm(dossier.name)
        if target == peer_name or target in peer_name or peer_name in target:
            return dossier, evaluation
    return None


def _flag(code: str, sev: QCSeverity, status: QCStatus, msg: str, rec: str) -> QCFlag:
    return QCFlag(code=code, severity=sev, status=status, message=msg, recommendation=rec)


def run_hierarchy_qc(
    dossier: JobDossier,
    selections: FactorSelections,
    score: ScoreResult,
    peers: list[tuple[JobDossier, Evaluation]],
) -> list[QCFlag]:
    """QC-флаги иерархии. `peers` — другие должности системы с их последними оценками."""
    flags: list[QCFlag] = []
    scored_peers = [(d, e) for d, e in peers if e.score is not None and d.id != dossier.id]

    # 1) Подчинённый не выше руководителя по управленческому уровню.
    if dossier.reporting.manager:
        found = _find_peer(dossier.reporting.manager, scored_peers)
        if found and found[1].selections is not None:
            mgr_dossier, mgr_eval = found
            own_mgmt = _MGMT_ORDER[selections.know_how.management.value]
            mgr_mgmt = _MGMT_ORDER[mgr_eval.selections.know_how.management.value]
            ok = own_mgmt < mgr_mgmt
            flags.append(
                _flag(
                    "subordinate_not_above_manager", QCSeverity.MEDIUM,
                    QCStatus.PASS if ok else QCStatus.WARN,
                    f"Управленческий уровень {selections.know_how.management.value} "
                    f"ниже уровня руководителя «{mgr_dossier.name}» "
                    f"({mgr_eval.selections.know_how.management.value})" if ok
                    else f"Управленческий уровень {selections.know_how.management.value} "
                    f"не ниже уровня руководителя «{mgr_dossier.name}» "
                    f"({mgr_eval.selections.know_how.management.value})",
                    "—" if ok
                    else "Нужно сильное матричное/экспертное обоснование, иначе пересмотреть "
                    "управленческий уровень (раздел 9.5).",
                )
            )

            manager = mgr_eval.selections
            manager_score = mgr_eval.score
            conflicts: list[str] = []
            if _MGMT_ORDER[selections.know_how.management.value] > _MGMT_ORDER[manager.know_how.management.value]:
                conflicts.append(
                    f"управленческие знания {selections.know_how.management.value} > "
                    f"{manager.know_how.management.value}"
                )
            if manager_score and score.problem_solving.percentage > manager_score.problem_solving.percentage:
                conflicts.append(
                    f"Problem Solving {score.problem_solving.percentage}% > "
                    f"{manager_score.problem_solving.percentage}%"
                )
            if _LETTER_ORDER[selections.accountability.freedom.value] > _LETTER_ORDER[manager.accountability.freedom.value]:
                conflicts.append(
                    f"свобода действий {selections.accountability.freedom.value} > "
                    f"{manager.accountability.freedom.value}"
                )
            flags.append(
                _flag(
                    "hierarchy_sensitive_factors",
                    QCSeverity.MEDIUM if conflicts else QCSeverity.LOW,
                    QCStatus.WARN if conflicts else QCStatus.PASS,
                    (f"Иерархически чувствительные показатели выше руководителя «{mgr_dossier.name}»: "
                     + "; ".join(conflicts)) if conflicts
                    else f"Управленческие знания, Problem Solving и свобода действий согласованы с уровнем руководителя «{mgr_dossier.name}»",
                    "Проверить традиционность или матричность структуры и обосновать исключение; "
                    "более глубокие специальные знания эксперта сами по себе не являются ошибкой."
                    if conflicts else "—",
                )
            )

    # 2) Сравнение с якорями: дистанция в грейдах и совпадение профиля.
    matched = 0
    for anchor_name in dossier.anchor_roles:
        found = _find_peer(anchor_name, scored_peers)
        if not found:
            continue
        matched += 1
        anchor_dossier, anchor_eval = found
        if anchor_eval.score is None:
            continue
        distance = steps_15pct(score.total_points, anchor_eval.score.total_points)
        if distance >= 3:
            flags.append(
                _flag(
                    "anchor_grade_gap", QCSeverity.MEDIUM, QCStatus.WARN,
                    f"Разрыв с якорем «{anchor_dossier.name}»: {distance} шагов по 15% "
                    f"({score.total_points} против {anchor_eval.score.total_points} баллов; "
                    f"грейды {score.grade} и {anchor_eval.score.grade})",
                    "Проверить, подтверждается ли расстояние различиями в содержании роли, "
                    "и провести калибровку по семье должностей.",
                )
            )

    # 3) Якоря заявлены, но в системе не оценены — калибровка невозможна.
    if dossier.anchor_roles and matched == 0:
        flags.append(
            _flag(
                "anchors_not_in_system", QCSeverity.LOW, QCStatus.WARN,
                "Якорные должности заявлены, но не найдены среди оценённых в системе — "
                "автоматическая калибровка не проводилась",
                "Оценить якорные должности в системе или провести калибровку вручную "
                "на Оценочном комитете.",
            )
        )
    elif matched > 0:
        flags.append(
            _flag(
                "anchor_calibration", QCSeverity.LOW, QCStatus.PASS,
                f"Калибровка выполнена по {matched} якорной(ым) должности(ям) из системы",
                "—",
            )
        )

    return flags
