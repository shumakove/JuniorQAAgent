from agent.state import AgentState
from agent.validator import validate_action
from agent.tools import (
    run_test,
    run_related_tests,
    get_test_history,
    get_pr_diff,
    get_ci_logs,
    run_test_sequence
)

MAX_ITERRATIONS = 6

def invistigate(state: AgentState) -> AgentState:
    while state.iteration < MAX_ITERRATIONS and not state.finished:
        state.iteration += 1

        if not state.ci_logs:
            state.ci_logs = get_ci_logs()
            state.actions_taken.append("get_ci_logs")
            continue

        if not state.test_runs:
            result = run_test(
                state.test_name,
                run_number=1
                )
            state.test_runs.append(result)
            state.actions_taken.append("run_test")
            continue

        latest_run = state.test_runs[-1]

        if latest_run["status"] == "PASSED":
            state.test_history = get_test_history(state.test_name)
            state.actions_taken.append("get_test_history")

            state.hypotesis = "Possible flaky test"
            state.confidence = 0.7

            break

        if latest_run["status"] == "FAILED":
            state.git_diff = get_pr_diff()
            state.actions_taken.append("get_pr_diff")

            state.hypothesis = "Possible application defect"
            state.confidence = 0.6

            break
    return state

def build_agent_context(state: AgentState) -> str:
    return f"""
You are a Quality Engineering investigation agent.

Your goal is to investigate a CI test failure.

Test:
{state.test_name}

Initial error:
{state.initial_error}

CI logs:
{state.ci_logs or "Not collected yet"}

Git diff:
{state.git_diff or "Not collected yet"}

Test runs:
{state.test_runs}

Test history:
{state.test_history}

Related tests:
{state.related_tests}

Current hypothesis:
{state.hypothesis or "None"}

Actions already taken:
{state.actions_taken}

Available tools:
- get_ci_logs
- get_pr_diff
- get_test_history
- run_test
- run_related_tests
- classify
- finish

For classify, use one of:
- ENVIRONMENT_FAILURE
- APPLICATION_BUG
- TEST_ISSUE
- FLAKY_TEST
- HUMAN_ESCALATION

Choose the next action based on the available evidence.
Do not invent evidence.
Use only the available tools.
If there is not enough evidence to continue safely, recommend HUMAN_ESCALATION.
"""

def execute_action(state, action):
    valid, error = validate_action(action)

    if not valid:
        state.hypothesis = f"Invalid agent action: {error}"
        state.human_escalation = True
        return

    if action.tool == "get_ci_logs":
        result = get_ci_logs()
        state.ci_logs = result

    elif action.tool == "get_pr_diff":
        result = get_pr_diff()
        state.git_diff = result

    elif action.tool == "get_test_history":
        result = get_test_history(
            action.arguments["test_name"]
        )
        state.test_history = result

    elif action.tool == "run_test":
        result = run_test_sequence(
            action.arguments["test_name"],
            action.arguments["run_number"],
        )
        state.test_runs.append(result)

    elif action.tool == "run_related_tests":
        result = run_related_tests(
            action.arguments["test_name"]
        )
        state.related_tests = result

    elif action.tool == "classify":
        classification = action.arguments["classification"]

        state.final_classification = action.arguments["classification"]
        state.confidence = action.arguments["confidence"]
        state.evidence = action.arguments["evidence"]

        if classification == "HUMAN_ESCALATION":
            state.human_escalation = True
        state.finished = True

       
    elif action.tool == "finish":
        state.finished = True


def run_agent(state, llm):
    while state.iteration < MAX_ITERRATIONS and not state.finished:
        state.iteration += 1

        context = build_agent_context(state)

        action = llm.decide(context, state)
        state.actions_taken.append(action.tool)
        execute_action(state, action)

        if state.human_escalation:
            break

    return state