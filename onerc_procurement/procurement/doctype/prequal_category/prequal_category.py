import frappe
from frappe.model.document import Document


class PrequalCategory(Document):
	def before_save(self):
		if not self.default_fee:
			settings = frappe.get_doc("Organisation Settings", "9krtu07qc3")
			self.default_fee = settings.default_fee or 5000
