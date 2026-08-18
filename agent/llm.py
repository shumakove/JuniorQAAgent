import json
from openai import OpenAI 
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

class OpenAILLM:
    def __init__(self, model: str = "gpt-5.6"):
        self.client = OpenAI()
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