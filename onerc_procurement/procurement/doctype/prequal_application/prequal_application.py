import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class PrequalApplication(Document):
	def before_save(self):
		self.last_edited = now_datetime()

	def is_editable(self):
		if self.edit_locked:
			return False
		exercise = frappe.get_doc("Prequal Exercise", self.exercise)
		if exercise.close_date and now_datetime() > exercise.close_date:
			return False
		if exercise.edit_cutoff_date and now_datetime() > exercise.edit_cutoff_date:
			return False
		return True

	def on_payment_confirmed(self):
		self.payment_status = "Paid"
		self.status = "Active"
		self.payment_date = now_datetime()
		self.save(ignore_permissions=True)
