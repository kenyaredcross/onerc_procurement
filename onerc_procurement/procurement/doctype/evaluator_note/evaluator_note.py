import frappe
from frappe.model.document import Document
from frappe.utils import now_datetime


class EvaluatorNote(Document):
	def before_save(self):
		if not self.note_date:
			self.note_date = now_datetime()
		if not self.evaluator:
			self.evaluator = frappe.session.user
