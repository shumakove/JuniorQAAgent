import json
from openai import OpenAI 
from ollama import Client
from agent.action import AgentAction

class FakeLLM:
    def decide(self, context: str) -> AgentAction:
        return AgentAction(
            tool="run_test",
            arguments= {
                "test_name": "test_checkout_payment",
                "run_number": 2,
            },
            reasoning="Reproduce the failure before gathering more evidence.",
        )

class FakeLoopLLM:
    def __init__(self):
        self.calls = 0

    def decide(self, context, state):
        self.calls += 1

        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments={},
                reasoning="I need CI evidence first.",
            )

        if len(state.test_runs) == 0:
            return AgentAction(
                tool="run_test",
                arguments={
                    "test_name": state.test_name,
                    "run_number": 1,
                },
                reasoning="I need to reproduce the failure.",
            )

        if len(state.test_runs) == 1:
            return AgentAction(
                tool="run_test",
                arguments={
                    "test_name": state.test_name,
                    "run_number": 2,
                },
                reasoning="The first reproduction failed, so I will rerun the test.",
            )

        if "get_test_history" not in state.actions_taken:
            return AgentAction(
                tool="get_test_history",
                arguments={
                    "test_name": state.test_name,
                },
                reasoning="I need historical evidence to assess whether this is a flaky test.",
            )

        return AgentAction(
                tool="classify",
                arguments={
                    "classification": "FLAKY_TEST",
                    "confidence": 0.87,
                    "evidence": [
                        "Initial CI run failed",
                        "Immediate rerun passed",
                        "Historical test results show intermittent failures",
                    ],
                },
                reasoning=(
                    "The failure is inconsistent and historical evidence "
                    "indicates that the test is flaky."
                ),
            )

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

class TestIssueFakeLLM:
    def decide(self, context, state: AgentState):
        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments= {},
                reasoning="I need CI evidence first"
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

class HumanEscalationFakeLLM:
    def decide(self, context, state: AgentState):
        if not state.ci_logs:
            return AgentAction(
                tool="get_ci_logs",
                arguments={},
                reasoning="I need CI evidence first"
            )
        if not state.git_diff:
            return AgentAction(
                tool="get_pr_diff",
                arguments={},
                reasoning="Getting PR to see what was changed"
            )
        if not state.test_history:
            return AgentAction(
                tool="get_test_history",
                arguments={
                    "test_name": "test_payment"
                },
                reasoning="Check history for previous executons status"
            )
        return AgentAction(
            tool="classify",
            arguments={
                "classification": "HUMAN_ESCALATION",
                "confidence": 0.95,
                "evidence": [
                    "CI logs do not identify a clear failure cause",
                    "PR diff does not provide sufficient evidence",
                    "Test history is insufficient to establish a pattern"
                ]
            },
            reasoning="Not enough information."
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

class OpenAILLM:
    def __init__(self, model: str = "llama3"):
        self.client = OpenAI(
            base_url="http://localhost:11434/v1",
            api_key="not_needed"
        )
        self.model = model

    def decide(self, context: str) -> AgentAction:
        response = self.client.responses.create(
            model=self.model,
            input=context,
            text={
                "format": {
                    "type": "json_schema",
                    "name": "agent_action",
                    "strict": True,
                    "schema": {
                        "type": "object",
                        "properties": {
                            "tool": {
                                "type": "string",
                                "enum": [
                                    "get_ci_logs",
                                    "get_pr_diff",
                                    "get_test_history",
                                    "run_test",
                                    "run_related_tests",
                                    "classify",
                                    "finish",
                                ],
                            },
                            "arguments": {
                                "type": "object",
                                "properties": {
                                    "test_name": {
                                        "type": "string"
                                    },
                                    "run_number": {
                                        "type": "integer"
                                    }
                                },
                                "required": [
                                    "test_name",
                                    "run_number"
                                ],
                                "additionalProperties": False,
                            },
                            "reasoning": {
                                "type": "string",
                            },
                        },
                        "required": [
                            "tool",
                            "arguments",
                            "reasoning",
                        ],
                        "additionalProperties": False,
                    },
                }
            },
        )

        data = json.loads(response.output_text)

        return AgentAction(
            tool=data["tool"],
            arguments=data["arguments"],
            reasoning=data["reasoning"],
        )

class OllamaLLM:

    AGENT_ACTION_SCHEMA = {
        "type": "object",
        "properties": {
            "tool": {
                "type": "string",
                "enum": [
                    "get_ci_logs",
                    "get_pr_diff",
                    "get_test_history",
                    "run_test",
                    "run_related_tests",
                    "classify",
                    "finish",
                ],
            },
            "arguments": {
                "type": "object",
                "properties": {
                    "test_name": {
                        "type": "string"
                    },
                    "run_number": {
                        "type": "integer"
                    },
                },
                "required": [
                    "test_name",
                    "run_number"
                ],
                "additionalProperties": False,
            },
            "reasoning": {
                "type": "string",
            },
        },
        "required": [
            "tool",
            "arguments",
            "reasoning",
        ],
        "additionalProperties": False,
    }
    def __init__(self, model="llama3.1"):
        self.client = Client()
        self.model = model

    def decide(self,context: str) -> AgentAction:
        response = self.client.chat(
            model=self.model,
            messages=[
                {'role':'user',
                  'content':context}
                  ],
            format=self.AGENT_ACTION_SCHEMA,
        )

        data = json.loads(response.message.content)
  
        return AgentAction(
            tool=data["tool"],
            arguments=data["arguments"],
            reasoning=data["reasoning"],
        )