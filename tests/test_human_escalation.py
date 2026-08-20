from agent.state import AgentState
from agent.action import AgentAction
from agent.agent import run_agent
from agent.llm import HumanEscalationFakeLLM

def test_human_escalation():
    state = AgentState(
        test_name="some_test",
        initial_error="unknown error"
    )

    llm = HumanEscalationFakeLLM()
    result = run_agent(state, llm)
    assert result.final_classification == "HUMAN_ESCALATION"
    assert result.human_escalation is True
    assert result.finished is True

    assert result.actions_taken == [
        "get_ci_logs",
        "get_pr_diff",
        "get_test_history",
        "classify",
    ]