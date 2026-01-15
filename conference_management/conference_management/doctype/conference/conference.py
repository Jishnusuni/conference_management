# Copyright (c) 2026, jishnusuni and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document
from frappe.utils import today


class Conference(Document):
	def validate(self):
		self.update_status()
		# self.validate_session_time_overlap()
	
	def update_status(self):
		if self.status == "Cancelled":
			return
		if today() < self.start_date:
			self.status = "Upcoming"
		elif self.start_date <= today() <= self.end_date:
			self.status = "Ongoing"
		else:
			self.status = "Completed"
