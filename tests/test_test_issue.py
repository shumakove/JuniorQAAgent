from agent.state import AgentState
from agent.action import AgentAction
from agent.agent import run_agent
class FakeLLM:

    def decide(self, context, state: AgentState):
        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments= {},
                reasoning="I need CI evidence ffirst"
            )
        if len(state.test_runs) < 2:
            return AgentAction(
                tool="run_test",
                arguments={
                    "test_name": state.test_name,
                    "run_number": len(state.test_runs) + 1,
                },
                reasoning="I need to reproduce the failure.",
            )
        if not state.test_history:
            return AgentAction(
                tool="get_test_history",
                arguments={
                    "test_name": "test_payment"
                },
                reasoning="Check history for previous executons status"
            )
        if not state.related_tests:
            return AgentAction(
                tool="run_related_tests",
                arguments={
                    "test_name": "test_related_feature"
                },
                reasoning="Trying to get test evidence for related tests"
            )
        return AgentAction(
            tool="classify",
            arguments={
                "classification": "TEST_ISSUE",
                "confidence": 0.91,
                    "evidence": [
                    "Initial test failure was not reproduced on rerun",
                    "Test history shows stable application behaviour",
                    "Related application tests passed"
                ]
            },
            reasoning="Problem is in the test"
        )

def test_test_issue():
    state = AgentState(
        test_name= "some_test",
        initial_error="Assertion in test"
    )
    llm = FakeLLM()
    result = run_agent(state,llm)

    print("\nFINAL STATE:")
    print("iteration:", result.iteration)
    print("actions:", result.actions_taken)
    print("test_runs:", result.test_runs)
    print("test_history:", result.test_history)
    print("related_tests:", result.related_tests)
    print("finished:", result.finished)
    print("human_escalation:", result.human_escalation)
    print("classification:", result.final_classification)
    print("hypothesis:", result.hypothesis)

    assert result.actions_taken == [
        "get_ci_logs",
        "run_test",
        "run_test",
        "get_test_history",
        "run_related_tests",
        "classify",
    ]

    assert result.final_classification == "TEST_ISSUE"
    assert result.confidence == 0.91
    assert result.finished is True
    assert result.human_escalation is False