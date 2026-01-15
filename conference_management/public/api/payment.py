import frappe
import random

@frappe.whitelist(allow_guest=True)
def process_payment(registration_id):
    """
    Simulate payment processing for a registration.
    Allows retry if previous payment failed.
    """

    if not registration_id:
        frappe.throw("Registration ID is required.")

    registration = frappe.get_doc("Registration", registration_id)

    # Do not allow payment retry if already paid
    if registration.payment_status == "Paid":
        return {
            "registration_id": registration.name,
            "payment_status": "Paid",
            "message": "Payment already completed."
        }

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

    return {
        "registration_id": registration.name,
        "payment_status": registration.payment_status,
        "message": message
    }


def mock_payment_gateway():
    return random.choice([True, True, True, True, False])
