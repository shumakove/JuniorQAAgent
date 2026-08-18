def get_ci_logs() -> str:
    return """
CI Job: checkout-tests

Test: test_checkout_payment

Error:
Timeout waiting for "Payment successful"

Application logs:
PaymentService: request started
PaymentService: waiting for payment provider
PaymentService: timeout after 30 seconds
"""

def get_pr_diff() -> str:
    return """
Modified files:

payment_service.py
checkout_controller.py

Changes:

payment_service.py:
- increased payment provider timeout
- changed retry handling

checkout_controller.py:
- updated payment status handling
"""

def get_test_history(test_name: str) -> list[dict]:
    return [
        {"run": 1, "status": "PASSED"},
        {"run": 2, "status": "PASSED"},
        {"run": 3, "status": "FAILED"},
        {"run": 4, "status": "PASSED"},
        {"run": 5, "status": "PASSED"},
    ]

def run_test(test_name: str, run_number: int) -> dict:
    if run_number == 1:
        return {
            "test": test_name,
            "status": "PASSED",
            "error": None,
        }

    return {
        "test": test_name,
        "status": "FAILED",
        "error": 'Timeout waiting for "Payment successful"',
    }

def run_related_tests(test_name: str) -> list[dict]:
    return [
        {
            "test": "test_payment_status",
            "status": "FAILED",
            "error": "Payment status remained PENDING",
        },
        {
            "test": "test_payment_retry",
            "status": "FAILED",
            "error": "Retry limit exceeded",
        },
    ]

def run_test_sequence(test_name: str, run_number: int) -> dict:
    if run_number == 1:
        return {
            "test": test_name,
            "status": "FAILED",
            "error": 'Timeout waiting for "Payment successful"',
        }

    return {
        "test": test_name,
        "status": "PASSED",
        "error": None,
    }