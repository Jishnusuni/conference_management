import frappe
import random
from conference_management.public.api.utils import log_api_request

@frappe.whitelist(allow_guest=True)
def process_payment(registration_id):
    """
    Simulate payment processing for a registration.
    Allows retry if previous payment failed.
    """

    api_endpoint = "process_payment"
    method = "POST"
    request_body = {"registration_id": registration_id}

    try:
        # Validate registration ID
        if not registration_id:
            response = {"status": "error", "message": "Registration ID is required."}
            log_api_request(api_endpoint, method, request_body, response, 400)
            return response

        registration = frappe.get_doc("Registration", registration_id)

        # Do not allow payment retry if already paid
        if registration.payment_status == "Paid":
            response = {
                "status": "success",
                "registration_id": registration.name,
                "payment_status": "Paid",
                "message": "Payment already completed."
            }
            log_api_request(api_endpoint, method, request_body, response, 200)
            return response

        # Process payment for Pending or Failed status
        payment_success = mock_payment_gateway()

        if payment_success:
            registration.payment_status = "Paid"
            message = "Payment completed successfully."
        else:
            registration.payment_status = "Failed"
            message = "Payment failed. You may retry the payment."

        registration.save(ignore_permissions=True)
        frappe.db.commit()

        # Successful payment response
        response = {
            "status": "success",
            "registration_id": registration.name,
            "payment_status": registration.payment_status,
            "message": message
        }
        log_api_request(api_endpoint, method, request_body, response, 200)
        return response

    except frappe.DoesNotExistError:
        response = {"status": "error", "message": "Registration not found."}
        log_api_request(api_endpoint, method, request_body, response, 404)
        return response

    except Exception as e:
        response = {"status": "error", "message": "Internal Server Error"}
        log_api_request(api_endpoint, method, request_body, response, 500)
        frappe.log_error(frappe.get_traceback(), "Process Payment API Error")
        return response


def mock_payment_gateway():
    """
    Mock payment gateway simulation.
    Returns True for success, False for failure.
    Success rate: 80%
    """
    return random.choice([True, True, True, True, False])
