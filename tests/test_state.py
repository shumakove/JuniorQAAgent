from agent.state import AgentState


def test_agent_state():
    state = AgentState(
        test_name="test_checkout_payment",
        initial_error='Timeout waiting for "Payment successful"',
    )

    assert state.test_name == "test_checkout_payment"
    assert state.iteration == 0
    assert state.confidence == 0.0
    assert state.final_classification is None