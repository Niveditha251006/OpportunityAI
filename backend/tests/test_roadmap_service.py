
from app.services.roadmap_service import estimate_task_minutes


def test_regular_task_uses_daily_study_time():
    assert estimate_task_minutes("Advanced SQL", 15) == 15
    assert estimate_task_minutes("Advanced SQL", 45) == 45


def test_portfolio_project_gets_extra_time():
    assert estimate_task_minutes("Portfolio project", 45) == 68


def test_capstone_duration_is_capped():
    assert estimate_task_minutes("Capstone analysis", 60) == 90


def test_short_sessions_have_minimum_duration():
    assert estimate_task_minutes("Advanced SQL", 5) == 10
