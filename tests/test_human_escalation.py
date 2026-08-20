from agent.state import AgentState
from agent.action import AgentAction
from agent.agent import run_agent

class FakeLLM:
    def decide(self, context, state: AgentState):
        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments={},
                reasoning="I need CI evidence first"
            )
        if not state.git_diff:
            return AgentAction(
                tool="get_pr_diff",
                arguments={},
                reasoning="Getting PR to see what was changed"
            )
        if not state.test_history:
            return AgentAction(
                tool="get_test_history",
                arguments={
                    "test_name": "test_payment"
                },
                reasoning="Check history for previous executons status"
            )
        return AgentAction(
            tool="classify",
            arguments={
                "classification": "HUMAN_ESCALATION",
                "confidence": 0.95,
                "evidence": [
                    "CI logs do not identify a clear failure cause",
                    "PR diff does not provide sufficient evidence",
                    "Test history is insufficient to establish a pattern"
                ]
            },
            reasoning="Not enough information."
        )

def test_human_escalation():
    state = AgentState(
        test_name="some_test",
        initial_error="unknown error"
    )

    llm = FakeLLM()
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