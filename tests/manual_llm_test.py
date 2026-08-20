from agent.agent import build_agent_context
from agent.llm import OllamaLLM
from agent.state import AgentState


state = AgentState(
    test_name="test_checkout_payment",
    initial_error='Timeout waiting for "Payment successful"',
)

state.ci_logs = """
CI Job: checkout-tests

Test: test_checkout_payment

Error:
Timeout waiting for "Payment successful"

Application logs:
PaymentService: request started
PaymentService: waiting for payment provider
PaymentService: timeout after 30 seconds
"""

state.actions_taken.append("get_ci_logs")

context = build_agent_context(state)

llm = OllamaLLM()

action = llm.decide(context)

print("Tool:", action.tool)
print("Arguments:", action.arguments)
print("Reasoning:", action.reasoning)