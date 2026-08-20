from agent.action import AgentAction
from agent.agent import run_agent
from agent.state import AgentState
from agent.llm import FakeLoopLLM

    
def test_agent_follows_investigation_sequence():
    state = AgentState(
        test_name="test_checkout_payment",
        initial_error="Timeout",
    )

    llm = FakeLoopLLM()

    result = run_agent(state, llm)

    assert result.actions_taken == [
        "get_ci_logs",
        "run_test",
        "run_test",
        "get_test_history",
        "classify",
    ]

    assert result.final_classification == "FLAKY_TEST"
    assert result.confidence == 0.87
    assert result.finished is True
    assert result.human_escalation is False

    assert result.evidence == [
        "Initial CI run failed",
        "Immediate rerun passed",
        "Historical test results show intermittent failures",
    ]