"""SqliteStore: персистентность Evaluation через настоящую БД, не InMemoryStore.

InMemoryStore (используемый в большинстве тестов) хранит Pydantic-объекты
напрямую и не проверяет, что save_evaluation/get_evaluation/list_evaluations
переживают сериализацию в JSON (``doc``) и обратно через реальный SQL.
"""

from __future__ import annotations

from jeval.domain.models import JobDossier
from jeval.orchestrator import JobEvaluator
from jeval.store import SqliteStore


def _sqlite_store(tmp_path):
    return SqliteStore(str(tmp_path / "jeval.db"))


def test_sqlite_store_round_trips_evaluation_via_job_evaluator(tmp_path, full_dossier, fake_agent):
    store = _sqlite_store(tmp_path)
    saved_position = store.save_position(full_dossier)

    evaluation = JobEvaluator(agent=fake_agent).evaluate(saved_position)
    evaluation.id = "ev-1"
    saved = store.save_evaluation(evaluation)
    assert saved.id == "ev-1"

    fetched = store.get_evaluation("ev-1")
    assert fetched is not None
    assert fetched.status == evaluation.status
    assert fetched.selections is not None
    assert fetched.selections.know_how.specialization == evaluation.selections.know_how.specialization
    assert fetched.score is not None
    assert fetched.score.total_points == evaluation.score.total_points
    assert fetched.score.grade == evaluation.score.grade
    assert fetched.score.table_version == evaluation.score.table_version

    listed = store.list_evaluations(position_id=saved_position.id)
    assert [e.id for e in listed] == ["ev-1"]


def test_sqlite_store_get_evaluation_missing_returns_none(tmp_path):
    store = _sqlite_store(tmp_path)
    assert store.get_evaluation("does-not-exist") is None


def test_sqlite_store_list_evaluations_filters_by_position(tmp_path, full_dossier, fake_agent):
    store = _sqlite_store(tmp_path)
    pos_a = store.save_position(full_dossier)
    pos_b = store.save_position(JobDossier(id="pos-2", name="Другая должность"))

    ev_a = JobEvaluator(agent=fake_agent).evaluate(pos_a)
    ev_a.id = "ev-a"
    store.save_evaluation(ev_a)

    ev_b = JobEvaluator(agent=fake_agent).evaluate(pos_b)
    ev_b.id = "ev-b"
    store.save_evaluation(ev_b)

    assert [e.id for e in store.list_evaluations(position_id=pos_a.id)] == ["ev-a"]
    assert [e.id for e in store.list_evaluations(position_id=pos_b.id)] == ["ev-b"]
    assert {e.id for e in store.list_evaluations()} == {"ev-a", "ev-b"}


def test_sqlite_store_save_evaluation_upserts_on_conflict(tmp_path, full_dossier, fake_agent):
    store = _sqlite_store(tmp_path)
    saved_position = store.save_position(full_dossier)

    evaluation = JobEvaluator(agent=fake_agent).evaluate(saved_position)
    evaluation.id = "ev-1"
    store.save_evaluation(evaluation)

    evaluation.recommendation = "Обновлённая рекомендация после пересмотра"
    store.save_evaluation(evaluation)

    listed = store.list_evaluations(position_id=saved_position.id)
    assert len(listed) == 1
    assert listed[0].recommendation == "Обновлённая рекомендация после пересмотра"
