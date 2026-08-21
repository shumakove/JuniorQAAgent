from agent.action import AgentAction
from agent.state import AgentState
from agent.agent import run_agent
class RealLoopLLM:

    def decide(self, context, state):

        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments={},
                reasoning="I need the CI logs first.",
            )

        if not state.git_diff:
            return AgentAction(
                tool="get_pr_diff",
                arguments={},
                reasoning="The failure requires additional repository evidence.",
            )

        return AgentAction(
            tool="classify",
            arguments={
                "classification": "APPLICATION_BUG",
                "confidence": 0.85,
                "evidence": [
                    "Observed failure in CI logs",
                    "Repository changes require investigation",
                ],
            },
            reasoning="Enough evidence to classify.",
        )

def test_agent_real_loop():
    llm = RealLoopLLM()
    state = AgentState(
        "test_1",
        initial_error="some error"
    )

    result = run_agent(state = state, llm = llm)

    assert result.actions_taken == [
    "get_ci_logs",
    "get_pr_diff",
    "classify"
]