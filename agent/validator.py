from agent.action import AgentAction

TOOL_ARGUMENTS = {
    "get_ci_logs": set(),
    "get_pr_diff": set(),
    "get_test_history": {"test_name"},
    "run_test": {"test_name", "run_number"},
    "run_related_tests": {"test_name"},
    "classify": {"classification", "confidence", "evidence"},
    "finish": set(),
}

VALID_CLASSIFICATIONS = {
    "ENVIRONMENT_FAILURE",
    "APPLICATION_BUG",
    "TEST_ISSUE",
    "FLAKY_TEST",
    "HUMAN_ESCALATION",
}

def validate_action(action: AgentAction) -> tuple[bool, str]:
    if action.tool not in TOOL_ARGUMENTS:
        return False, f"Unknown tool {action.tool}"
    expected_arguments = TOOL_ARGUMENTS[action.tool]
    actual_arguments = set(action.arguments.keys())

    if action.tool == "classify":
        classification = action.arguments.get("classification")

        if classification not in VALID_CLASSIFICATIONS:
            return (
                False,
                f"Invalid classification: {classification}",
            )

        confidence = action.arguments.get("confidence")

        if not isinstance(confidence, (int, float)):
            return False, "Confidence must be numeric."

        if not 0.0 <= confidence <= 1.0:
            return False, "Confidence must be between 0 and 1."
        evidence = action.arguments.get("evidence")

        if not isinstance(evidence, list):
            return False, "Evidence must be a list."

        if not all(isinstance(item, str) for item in evidence):
            return False, "Every evidence item must be a string."
        
    if actual_arguments != expected_arguments:
        return (False,
                f"Invalid arguments for {action.tool}. "
                f"Expected: {expected_arguments}, "
                f"got: {actual_arguments}"
                )
    return True, ""

