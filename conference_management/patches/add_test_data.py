import frappe
from frappe.utils import getdate, get_datetime
from datetime import timedelta
from datetime import datetime


def execute():
    conference = create_conference()
    sessions = create_sessions(conference)
    attendee = create_attendee()
    create_registration(conference.name, sessions[0].name, attendee.name)


def create_conference():
    existing = frappe.db.get_value(
        "Conference",
        {"conference_name": "Test Conference 2026"},
        "name"
    )
    if existing:
        return frappe.get_doc("Conference", existing)

    conference = frappe.get_doc({
        "doctype": "Conference",
        "conference_name": "Test Conference 2026",
        "start_date": datetime.strptime("2026-02-10", "%Y-%m-%d").date(),
        "end_date": datetime.strptime("2026-02-12", "%Y-%m-%d").date(),
        "location": "Chennai",
        "description": "Sample conference for testing"
    })
    conference.insert(ignore_permissions=True)
    return conference


def create_sessions(conference):
    session_docs = []

    # Convert date → datetime (00:00:00)
    base_dt = get_datetime(conference.start_date)

    sessions = [
        {
            "session_name": "Python Basics",
            "speaker": "Alice",
            "max_attendees": 50,
            "start_time": base_dt + timedelta(hours=10),
            "end_time": base_dt + timedelta(hours=12),
        },
        {
            "session_name": "Advanced Python",
            "speaker": "Bob",
            "max_attendees": 30,
            "start_time": base_dt + timedelta(hours=13),
            "end_time": base_dt + timedelta(hours=15),
        }
    ]

    for s in sessions:
        existing = frappe.db.get_value(
            "Session",
            {
                "conference": conference.name,
                "session_name": s["session_name"]
            },
            "name"
        )
        if existing:
            session_docs.append(frappe.get_doc("Session", existing))
            continue

        doc = frappe.get_doc({
            "doctype": "Session",
            "conference": conference.name,
            **s
        })
        doc.insert(ignore_permissions=True)
        session_docs.append(doc)

    return session_docs


def create_attendee():
    existing = frappe.db.get_value(
        "Attendee",
        {"email": "test.user@example.com"},
        "name"
    )
    if existing:
        return frappe.get_doc("Attendee", existing)

    attendee = frappe.get_doc({
        "doctype": "Attendee",
        "attendee_name": "Test User",
        "email": "test.user@example.com",
        "phone_number": "9999999999",
        "organization": "Test Org"
    })
    attendee.insert(ignore_permissions=True)
    return attendee


def create_registration(conference, session, attendee):
    if frappe.db.exists(
        "Registration",
        {
            "conference": conference,
            "session": session,
            "attendee": attendee
        }
    ):
        return

    registration = frappe.get_doc({
        "doctype": "Registration",
        "conference": conference,
        "session": session,
        "attendee": attendee,
        "registration_date": getdate(),
        "payment_status": "Pending"
    })
    registration.insert(ignore_permissions=True)
