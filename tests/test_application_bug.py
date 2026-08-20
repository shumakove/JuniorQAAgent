from agent.agent import run_agent
from agent.action import AgentAction
from agent.state import AgentState

class ApplicationBugFakeLLM:

    def decide(self, context, state):

        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments={},
                reasoning="I need CI evidence first.",
            )

        if len(state.test_runs) < 2:
            return AgentAction(
                tool="run_test",
                arguments={
                    "test_name": state.test_name,
                    "run_number": len(state.test_runs) + 1,
                },
                reasoning="The failure needs to be reproduced.",
            )

        if not state.git_diff:
            return AgentAction(
                tool="get_pr_diff",
                arguments={},
                reasoning="The failure reproduced, so I will inspect recent code changes.",
            )

        if not state.related_tests:
            return AgentAction(
                tool="run_related_tests",
                arguments={
                    "test_name": state.test_name,
                },
                reasoning="I will run related tests to determine whether the issue affects application behavior.",
            )

        return AgentAction(
            tool="classify",
            arguments={
                "classification": "APPLICATION_BUG",
                "confidence": 0.93,
                "evidence": [
                    "CI failure reproduced twice",
                    "Recent PR changed payment timeout configuration",
                    "Related payment tests also failed",
                ],
            },
            reasoning="The failure is reproducible and correlated with a recent application change.",
        )

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