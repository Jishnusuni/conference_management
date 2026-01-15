# Copyright (c) 2026, jishnusuni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import get_datetime, getdate


class Session(Document):

    def validate(self):
        # Entry point for all session validations
        self.validate_within_conference_dates()
        self.validate_datetime_overlap()

    def validate_within_conference_dates(self):
        """
        Ensure session datetime falls within
        the parent conference start and end dates.
        """
        conference = frappe.get_doc("Conference", self.conference)

        session_start_date = getdate(self.start_time)
        session_end_date = getdate(self.end_time)

        if session_start_date < conference.start_date:
            frappe.throw("Session start time is before the conference start date.")

        if session_end_date > conference.end_date:
            frappe.throw("Session end time is after the conference end date.")

    def validate_datetime_overlap(self):
        """
        Prevent overlapping sessions within the same conference.
        Overlap rule:
        new_start < existing_end AND new_end > existing_start
        """
        overlapping_sessions = frappe.db.sql("""
            SELECT name
            FROM `tabSession`
            WHERE conference = %s
              AND name != %s
              AND (%s < end_time AND %s > start_time)
        """, (
            self.conference,            # Same conference
            self.name or "",            # Exclude current session
            self.start_time,            # New session start datetime
            self.end_time               # New session end datetime
        ))

        if overlapping_sessions:
            frappe.throw(
                "Session time overlaps with another session scheduled "
                "in this conference."
            )
