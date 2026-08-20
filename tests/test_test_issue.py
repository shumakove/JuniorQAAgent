from agent.state import AgentState
from agent.action import AgentAction
from agent.agent import run_agent
from agent.llm import TestIssueFakeLLM


def test_test_issue():
    state = AgentState(
        test_name= "some_test",
        initial_error="Assertion in test"
    )
    llm = TestIssueFakeLLM()
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