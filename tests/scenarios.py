from dataclasses import dataclass
from agent.state import AgentState
from agent.llm import (
    FakeLLM, 
    FakeLoopLLM, 
    TestIssueFakeLLM, 
    ApplicationBugFakeLLM, 
    HumanEscalationFakeLLM, 
    EnvironmentFailureFakeLLM
)

@dataclass
class EvaluationScenario:
    name: str
    state_factory: callable
    llm_factory: callable
    expected_classification: str
    expected_actions: list[str]

flaky_scenario = EvaluationScenario(
    name="flaky_test",
    state_factory=lambda: AgentState(
        test_name="test_checkout_payment",
        initial_error="Timeout",
    ),

    llm_factory=lambda: FakeLoopLLM(),

    expected_classification="FLAKY_TEST",

    expected_actions=[
        "get_ci_logs",
        "run_test",
        "run_test",
        "get_test_history",
        "classify",
    ],
)

application_bug_scenario = EvaluationScenario(
    name="application_bug",
    state_factory=lambda: AgentState(
        test_name="test_checkout_payment",
        initial_error="Payment provider timeout",
    ),
    llm_factory=lambda: ApplicationBugFakeLLM(),
    expected_classification="APPLICATION_BUG",
    expected_actions=[
        "get_ci_logs",
        "run_test",
        "run_test",
        "get_pr_diff",
        "run_related_tests",
        "classify",
    ],
)

environment_failure_scenario = EvaluationScenario(
    name="environment_failure",
    state_factory=lambda: AgentState(
        test_name="test_checkout_payment",
        initial_error="Database connection failed",
    ),
    llm_factory=lambda: EnvironmentFailureFakeLLM(),
    expected_classification="ENVIRONMENT_FAILURE",
    expected_actions=[
        "get_ci_logs",
        "classify",
    ],
)

test_issue_scenario = EvaluationScenario(
    name="test_issue",
    state_factory=lambda: AgentState(
        test_name="some_test",
        initial_error="Timeout waiting for payment",
    ),
    llm_factory=lambda: TestIssueFakeLLM(),
    expected_classification="TEST_ISSUE",
    expected_actions=[
        "get_ci_logs",
        "run_test",
        "run_test",
        "get_test_history",
        "run_related_tests",
        "classify",
    ],
)

human_escalation_scenario = EvaluationScenario(
    name="human_escalation",
    state_factory=lambda: AgentState(
        test_name="some_test",
        initial_error="Unexpected error",
    ),
    llm_factory=lambda: HumanEscalationFakeLLM(),
    expected_classification="HUMAN_ESCALATION",
    expected_actions=[
        "get_ci_logs",
        "get_pr_diff",
        "get_test_history",
        "classify",
    ],
)

ALL_SCENARIOS = [
    flaky_scenario,
    application_bug_scenario,
    environment_failure_scenario,
    test_issue_scenario,
    human_escalation_scenario,
]