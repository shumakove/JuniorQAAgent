from agent.agent import run_agent
from tests.scenarios import ALL_SCENARIOS

def test_all_scenarios():

    total = len(ALL_SCENARIOS)
    classification_passed = 0
    trajectory_passed = 0
    total_actions = 0
    human_escalations = 0

    for scenario in ALL_SCENARIOS:
        state = scenario.state_factory()
        llm = scenario.llm_factory()

        result = run_agent(state, llm)

        print(f"\nScenario: {scenario.name}")
        print(f"Expected: {scenario.expected_classification}")
        print(f"Actual:   {result.final_classification}")
        print(f"Actions:  {result.actions_taken}")

        if result.final_classification == scenario.expected_classification:
            classification_passed += 1

        if result.actions_taken == scenario.expected_actions:
            trajectory_passed += 1

        total_actions += len(result.actions_taken)

        if result.human_escalation:
            human_escalations += 1

        assert result.final_classification == scenario.expected_classification
        assert result.actions_taken == scenario.expected_actions

    classification_accuracy = classification_passed / total
    trajectory_accuracy = trajectory_passed / total
    average_actions = total_actions / total
    escalation_rate = human_escalations / total

    print("\n==============================")
    print("AGENT EVALUATION")
    print("==============================")
    print(f"Scenarios:              {total}")
    print(f"Classification accuracy: {classification_accuracy:.0%}")
    print(f"Trajectory accuracy:     {trajectory_accuracy:.0%}")
    print(f"Average tool calls:      {average_actions:.2f}")
    print(f"Human escalation rate:   {escalation_rate:.0%}")