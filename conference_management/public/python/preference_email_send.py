import frappe
from frappe.utils import now_datetime


def send_scheduled_recommendations():
    print("-------called ----------")
    """
    Scheduler entry point.

    Runs automatically based on hooks.py configuration.
    Iterates through all attendees and sends speaker-based
    session recommendations.
    """
    # Fetch all attendees in the system
    attendees = frappe.get_all(
        "Attendee",
        pluck="name"
    )

    # Process recommendations for each attendee
    for attendee in attendees:
        send_recommendations_for_attendee(attendee)


def send_recommendations_for_attendee(attendee):
    """
    Sends session recommendations for a single attendee
    based ONLY on similar speakers.

    Flow:
    - Read attendee preferred sessions
    - Extract speakers from those sessions
    - Find upcoming sessions by the same speakers
    - Exclude already registered sessions
    - Send email notification
    """
    # Load attendee document
    attendee_doc = frappe.get_doc("Attendee", attendee)

    # Skip attendee if email is missing
    if not attendee_doc.email:
        return

    # Collect preferred sessions from attendee preferences child table
    preferred_sessions = [
        row.session for row in attendee_doc.preferences
    ]

    # If no preferences are defined, exit
    if not preferred_sessions:
        return

    # Fetch speakers from preferred sessions
    preferred_speakers = frappe.get_all(
        "Session",
        filters={"name": ["in", preferred_sessions]},
        pluck="speaker"
    )

    # Remove empty values and duplicates
    speakers = list({s for s in preferred_speakers if s})

    # If no valid speakers found, exit
    if not speakers:
        return

    # Fetch sessions already registered by the attendee
    # Failed registrations are ignored
    registered_sessions = frappe.get_all(
        "Registration",
        filters={
            "attendee": attendee,
            "payment_status": ["!=", "Failed"]
        },
        pluck="session"
    )

    # Find upcoming sessions by the same speakers
    # Exclude already registered sessions
    recommended_sessions = frappe.get_all(
        "Session",
        filters={
            "name": ["not in", registered_sessions],
            "start_time": [">", now_datetime()],
            "speaker": ["in", speakers]
        },
        fields=["session_name", "speaker"]
    )

    # If no matching sessions found, exit
    if not recommended_sessions:
        return

    # Build email content
    message = (
        "<p>Based on the speakers you follow, "
        "you may be interested in these upcoming sessions:</p><ul>"
    )

    for s in recommended_sessions:
        message += f"<li>{s.session_name} – {s.speaker}</li>"

    message += "</ul>"

    # Send recommendation email
    frappe.sendmail(
        recipients=[attendee_doc.email],
        subject="Sessions by Speakers You Follow",
        message=message
    )
