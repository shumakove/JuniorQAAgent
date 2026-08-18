from agent.action import AgentAction
from agent.validator import validate_action

def test_valid_run_test():
    action = AgentAction(
        tool="run_test",
        arguments={
            "test_name": "test_checkout_payment",
            "run_number": 2,
        },
        reasoning="Reproduce the failure.",
    )
    valid, error = validate_action(action)

    assert valid is True
    assert error == ""

def test_invalid_get_pr_diff_arguments():
    action = AgentAction(
        tool="get_pr_diff",
        arguments={
            "test_name": "test_checkout_payment",
            "run_number": 0,
        },
        reasoning="Inspect the PR.",
    )

    valid, error = validate_action(action)

    assert valid is False
    assert "Invalid arguments" in error


def test_unknown_tool():
    action = AgentAction(
        tool="delete_database",
        arguments={},
        reasoning="Cleanup.",
    )

    valid, error = validate_action(action)

    assert valid is False
    assert "Unknown tool" in error