import frappe
from frappe.utils import today
from conference_management.public.api.utils import log_api_request

@frappe.whitelist(allow_guest=True)
def get_attendee_recommendations(attendee):
    """
    Fetch recommended sessions for an attendee based on their preferences.

    Args:
        attendee (str): Attendee DocType name

    Returns:
        dict: Recommended sessions
    """

    api_endpoint = "get_attendee_recommendations"
    method = "GET"
    request_body = {"attendee": attendee}

    try:
        # Validate attendee exists
        if not attendee or not frappe.db.exists("Attendee", attendee):
            response = {"status": "error", "message": "Attendee not found."}
            log_api_request(api_endpoint, method, request_body, response, 400)
            return response

        # Fetch attendee document
        attendee_doc = frappe.get_doc("Attendee", attendee)

        # Collect preferred sessions from the child table
        preferred_sessions = [row.session for row in (attendee_doc.preferences or [])]

        # No preferences found
        if not preferred_sessions:
            response = {"status": "success", "recommendations": [], "message": "No preferences found."}
            log_api_request(api_endpoint, method, request_body, response, 200)
            return response

        # Fetch speakers of preferred sessions
        preferred_speakers = frappe.get_all(
            "Session",
            filters={"name": ["in", preferred_sessions]},
            fields=["speaker"]
        )
        speakers = list(set([p.speaker for p in preferred_speakers if p.speaker]))

        # Recommended sessions: upcoming sessions by same speakers, exclude already preferred sessions
        recommended_sessions = frappe.get_all(
            "Session",
            filters={
                "speaker": ["in", speakers],
                "name": ["not in", preferred_sessions],
                "start_time": [">=", today()]
            },
            fields=[
                "name",
                "session_name",
                "speaker",
                "start_time",
                "end_time",
                "conference"
            ],
            order_by="start_time asc"
        )

        # Successful response
        response = {
            "status": "success",
            "attendee": attendee,
            "recommendations": recommended_sessions
        }
        log_api_request(api_endpoint, method, request_body, response, 200)
        return response

    except Exception as e:
        # Handle unexpected errors
        response = {"status": "error", "message": "Internal Server Error"}
        log_api_request(api_endpoint, method, request_body, response, 500)
        frappe.log_error(frappe.get_traceback(), "Get Attendee Recommendations API Error")
        return response
