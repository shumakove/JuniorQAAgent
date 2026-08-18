from agent.llm import FakeLLM

def test_fake_llm_returns_action():
    fake_llm = FakeLLM()
    action = fake_llm.decide("fake context")

    assert action.tool == "run_test"
    assert action.arguments["test_name"] == "test_checkout_payment"
    