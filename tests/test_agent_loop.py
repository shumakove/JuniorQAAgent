from agent.action import AgentAction
from agent.agent import run_agent
from agent.state import AgentState


class FakeLoopLLM:
    def __init__(self):
        self.calls = 0

    def decide(self, context, state):
        self.calls += 1

        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments={},
                reasoning="I need CI evidence first.",
            )

        if len(state.test_runs) == 0:
            return AgentAction(
                tool="run_test",
                arguments={
                    "test_name": state.test_name,
                    "run_number": 1,
                },
                reasoning="I need to reproduce the failure.",
            )

        if len(state.test_runs) == 1:
            return AgentAction(
                tool="run_test",
                arguments={
                    "test_name": state.test_name,
                    "run_number": 2,
                },
                reasoning="The first reproduction failed, so I will rerun the test.",
            )

        if "get_test_history" not in state.actions_taken:
            return AgentAction(
                tool="get_test_history",
                arguments={
                    "test_name": state.test_name,
                },
                reasoning="I need historical evidence to assess whether this is a flaky test.",
            )

        return AgentAction(
                tool="classify",
                arguments={
                    "classification": "FLAKY_TEST",
                    "confidence": 0.87,
                    "evidence": [
                        "Initial CI run failed",
                        "Immediate rerun passed",
                        "Historical test results show intermittent failures",
                    ],
                },
                reasoning=(
                    "The failure is inconsistent and historical evidence "
                    "indicates that the test is flaky."
                ),
            )
    
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