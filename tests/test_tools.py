from agent.tools import (
    get_ci_logs,
    get_pr_diff,
    get_test_history,
    run_test,
    run_related_tests
)

def test_get_ci_logs():
    logs = get_ci_logs()

    assert "test_checkout_payment" in logs
    assert "Timeout" in logs


def test_get_pr_diff():
    diff = get_pr_diff()

    assert "payment_service.py" in diff


def test_get_test_history():
    history = get_test_history("test_checkout_payment")

    assert len(history) == 5


def test_run_test():
    result = run_test("test_checkout_payment", 1)

    assert result["status"] == "PASSED"


def test_run_related_tests():
    results = run_related_tests("test_checkout_payment")

    assert len(results) == 2
