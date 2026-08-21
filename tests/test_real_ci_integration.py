from agent.action import AgentAction
from agent.agent import run_agent_with_ci_log
from agent.state import AgentState


class RealCILogFakeLLM:

    def decide(self, context, state):

        if not state.git_diff:
            return AgentAction(
                tool="get_pr_diff",
                arguments={},
                reasoning="The CI log shows a failure, but more evidence is needed.",
            )

        return AgentAction(
            tool="classify",
            arguments={
                "classification": "APPLICATION_BUG",
                "confidence": 0.8,
                "evidence": [
                    "Real pytest failure was observed in CI log"
                ],
            },
            reasoning="Classify based on observed CI evidence.",
        )

def test_agent_reads_real_ci_log():

    state = AgentState(
        test_name="test_payment_timeout",
        initial_error="",
    )

    llm = RealCILogFakeLLM()

    result = run_agent_with_ci_log(
        state,
        llm,
        "ci.log",
    )

    assert "test_payment_timeout" in result.ci_logs
    assert "Timeout waiting for Payment successful" in result.ci_logs

    assert result.final_classification == "APPLICATION_BUG"
    assert result.finished is True