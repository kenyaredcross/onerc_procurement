import frappe
from frappe.model.document import Document


class ComplianceRecord(Document):
	def on_submit(self):
		self._compute_overall_status()
		self._update_application()

	def _compute_overall_status(self):
		for item in self.items:
			if item.is_mandatory and item.status not in ("Compliant", "Not Applicable"):
				self.overall_status = "Non-Compliant"
				return
		self.overall_status = "Compliant"

	def _update_application(self):
		if not self.application:
			return
		app = frappe.get_doc("Prequal Application", self.application)
		app.compliance_status = self.overall_status
		app.save(ignore_permissions=True)
