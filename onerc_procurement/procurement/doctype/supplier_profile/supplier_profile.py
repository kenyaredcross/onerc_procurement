import frappe
from frappe import _
from frappe.model.document import Document

_INTEGRITY_FIELDS = [
	"criminal_conviction",
	"terrorist_activities",
	"bankruptcy",
	"staff_conflict",
	"money_laundering",
	"politically_exposed",
]

_REQUIRED_FOR_COMPLETE = [
	"company_name",
	"organisation_type",
	"main_office_location",
	"contact_person_name",
	"contact_email",
	"contact_phone",
]


class SupplierProfile(Document):
	def validate(self):
		self._flag_integrity_issues()
		self._update_profile_status()

	def _flag_integrity_issues(self):
		flagged = [f for f in _INTEGRITY_FIELDS if self.get(f) == "Yes"]
		if flagged:
			labels = ", ".join(frappe.unscrub(f) for f in flagged)
			frappe.msgprint(
				_("Warning: The following integrity flags are set to Yes: {0}. This profile will be reviewed by compliance.").format(labels),
				alert=True,
				indicator="red",
			)

	def _update_profile_status(self):
		complete = all(self.get(f) for f in _REQUIRED_FOR_COMPLETE)
		if complete:
			if self.profile_status == "Incomplete":
				self.profile_status = "Complete"
		else:
			self.profile_status = "Incomplete"
