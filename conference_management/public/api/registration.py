# registration.py

import frappe
from frappe.utils import now_datetime
from conference_management.conference_management.doctype.registration.registration import Registration as RegistrationDoc

@frappe.whitelist(allow_guest=True)
def register_session(**kwargs):
    """
    Public API to register an attendee for a session.
    Accepts flexible arguments using **kwargs.

    Required kwargs:
        - attendee: Attendee DocType name
        - session: Session DocType name
        - conference: Conference DocType name

    Optional kwargs can include:
        - any custom fields for Registration

    Returns:
        dict: Registration status and payment outcome
    """

    # Extract required fields from kwargs
    attendee = kwargs.get("attendee")
    session = kwargs.get("session")
    conference = kwargs.get("conference")

    # Validate required fields
    if not attendee or not frappe.db.exists("Attendee", attendee):
        return {"status": "error", "message": "Attendee not found."}
    if not session or not frappe.db.exists("Session", session):
        return {"status": "error", "message": "Session not found."}
    if not conference or not frappe.db.exists("Conference", conference):
        return {"status": "error", "message": "Conference not found."}

    # Build Registration document
    reg_doc_dict = {
        "doctype": "Registration",
        "attendee": attendee,
        "session": session,
        "conference": conference,
        "registration_date": now_datetime(),
        "payment_status": "Pending"
    }

    reg_doc = frappe.get_doc(reg_doc_dict)

    try:
        # Insert registration and trigger validations
        reg_doc.insert(ignore_permissions=True)

        return {
            "status": "success",
            "registration": reg_doc.name,
            "payment_status": reg_doc.payment_status
        }

    except frappe.ValidationError as e:
        return {"status": "error", "message": str(e)}
