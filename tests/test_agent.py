from agent.agent import invistigate
from agent.state import AgentState

ALLOWED_TOOLS = {
    "get_ci_logs",
    "get_pr_diff",
    "get_test_history",
    "run_test",
    "run_related_tests",
}

def test_invistigate_failure():
    state = AgentState(
        test_name="test_checkout_payment",
        initial_error='Timeout waiting for "Payment successful"',
    )

    result = invistigate(state)
    assert result.iteration > 0
    assert len(result.actions_taken) > 0
    assert result.ci_logs != ""

