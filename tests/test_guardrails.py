from agent.action import AgentAction
from agent.state import AgentState
from agent.agent import run_agent

class InvalidActionLLM:

    def decide(self, context, state):

        return AgentAction(
            tool="run_test",
            arguments={},
            reasoning="Let's rerun the test."
        )

def test_guardrails():
    llm = InvalidActionLLM()
    state = AgentState(
        test_name="some_test",
        initial_error="some initial error"
    )

    result = run_agent(state, llm)

    assert result.human_escalation is True
    assert result.finished is False
    assert result.final_classification is None