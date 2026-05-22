import frappe
from frappe import _
from frappe.model.document import Document


class EvaluationPanel(Document):
	def before_save(self):
		if self.exercise and self.category:
			self.panel_name = f"{self.exercise} - {self.category}"

	def validate(self):
		member_users = [m.user for m in self.members]
		if self.lead_evaluator and self.lead_evaluator not in member_users:
			frappe.throw(_("Lead Evaluator {0} must also be listed in the Members table").format(self.lead_evaluator))
