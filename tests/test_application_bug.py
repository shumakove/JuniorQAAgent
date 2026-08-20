from agent.agent import run_agent
from agent.action import AgentAction
from agent.state import AgentState
from agent.llm import ApplicationBugFakeLLM

def test_agent_detects_application_bug():

    state = AgentState(
        test_name="test_checkout_payment",
        initial_error="Payment provider timeout",
    )

    llm = ApplicationBugFakeLLM()

    result = run_agent(state, llm)

    print("\nFINAL STATE:")
    print("actions:", result.actions_taken)
    print("ci_logs:", result.ci_logs)
    print("test_runs:", result.test_runs)
    print("git_diff:", result.git_diff)
    print("related_tests:", result.related_tests)
    print("hypothesis:", result.hypothesis)
    print("confidence:", result.confidence)
    print("human_escalation:", result.human_escalation)
    print("finished:", result.finished)
    print("classification:", result.final_classification)
    
    assert result.actions_taken == [
        "get_ci_logs",
        "run_test",
        "run_test",
        "get_pr_diff",
        "run_related_tests",
        "classify",
    ]

    assert result.final_classification == "APPLICATION_BUG"
    assert result.confidence == 0.93
    assert result.finished is True
    assert result.human_escalation is False