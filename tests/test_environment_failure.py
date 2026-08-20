from agent.state import AgentState
from agent.agent import run_agent
from agent.action import AgentAction
from agent.tools import (
    get_ci_logs
)
class EnvironmentFailureFakeLLM:

    def decide(self, context, state: AgentState):

        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments= {},
                reasoning="I need CI evidence ffirst"
            )
        return AgentAction(
            tool="classify",
            arguments={
                "classification": "ENVIRONMENT_FAILURE",
                "confidence": 0.98,
                "evidence": [
                    "CI logs show database connection failure",
                    "DNS resolution failed",
                    "The failure is infrastructure-related"
                ]
            },
            reasoning="There is environment issue in CI evidence"
        ) 
            
def test_environment_failue():
    state = AgentState(
        test_name= "test_modules_connection",
        initial_error="Connection time out"
    )
    llm = EnvironmentFailureFakeLLM()

    result = run_agent(state, llm)

    assert result.actions_taken == [
        "get_ci_logs",
        "classify"
    ]

    assert result.final_classification == "ENVIRONMENT_FAILURE"
    assert result.confidence == 0.98
    assert result.finished == True
    assert result.human_escalation is False