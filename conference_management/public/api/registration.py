# registration.py

import frappe
from frappe.utils import now_datetime
from conference_management.conference_management.doctype.registration.registration import Registration as RegistrationDoc
from conference_management.public.api.utils import log_api_request


@frappe.whitelist(allow_guest=True)
def register_session(**kwargs):
    api_endpoint = "register_session"
    method = "POST"
    request_body = kwargs

    try:
        # 1. Required fields
        attendee = kwargs.get("attendee")
        session = kwargs.get("session")
        conference = kwargs.get("conference")

        if not attendee or not frappe.db.exists("Attendee", attendee):
            response = {"status": "error", "message": "Attendee not found."}
            log_api_request(api_endpoint, method, request_body, response, 400)
            return response

        if not session or not frappe.db.exists("Session", session):
            response = {"status": "error", "message": "Session not found."}
            log_api_request(api_endpoint, method, request_body, response, 400)
            return response

        if not conference or not frappe.db.exists("Conference", conference):
            response = {"status": "error", "message": "Conference not found."}
            log_api_request(api_endpoint, method, request_body, response, 400)
            return response

        # 2. Create Registration document
        reg_doc_dict = {
            "doctype": "Registration",
            "attendee": attendee,
            "session": session,
            "conference": conference,
            "registration_date": now_datetime(),
            "payment_status": "Pending"
        }

        # Merge optional kwargs
        for key, value in kwargs.items():
            if key not in ["attendee", "session", "conference"]:
                reg_doc_dict[key] = value

        reg_doc = frappe.get_doc(reg_doc_dict)

        # 3. Insert registration (triggers validate hooks)
        reg_doc.insert(ignore_permissions=True)
        reg_doc.submit()

        # 4. Success response
        response = {
            "status": "success",
            "registration": reg_doc.name,
            "payment_status": reg_doc.payment_status
        }
        log_api_request(api_endpoint, method, request_body, response, 200)
        return response

    except frappe.ValidationError as e:
        response = {"status": "error", "message": str(e)}
        log_api_request(api_endpoint, method, request_body, response, 400)
        return response

    except Exception as e:
        response = {"status": "error", "message": "Internal Server Error"}
        log_api_request(api_endpoint, method, request_body, response, 500)
        frappe.log_error(frappe.get_traceback(), "API Error")
        return response
