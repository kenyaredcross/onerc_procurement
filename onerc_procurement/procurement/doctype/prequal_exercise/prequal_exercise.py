import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class PrequalExercise(Document):
	def validate(self):
		self._validate_dates()
		self._validate_unique_categories()

	def _validate_dates(self):
		if self.open_date and self.close_date:
			if self.open_date >= self.close_date:
				frappe.throw(_("Open Date must be before Close Date"))
		if self.edit_cutoff_date and self.close_date:
			if self.edit_cutoff_date > self.close_date:
				frappe.throw(_("Edit Cutoff Date cannot be after Close Date"))

	def _validate_unique_categories(self):
		seen = []
		for row in self.categories:
			if row.category in seen:
				frappe.throw(_("Duplicate category {0} in exercise").format(row.category))
			seen.append(row.category)

	def publish(self):
		self.status = "Published"
		self.save()

	def close_exercise(self):
		self.status = "Closed"
		self.save()

	def update_statistics(self):
		apps = frappe.get_all(
			"Prequal Application",
			filters={"exercise": self.name},
			fields=["status", "is_responsive", "pass_fail"],
		)
		self.total_bids = len(apps)
		self.responsive_bids = sum(1 for a in apps if a.is_responsive)
		self.non_responsive_bids = sum(1 for a in apps if not a.is_responsive)
		self.prequalified_count = sum(1 for a in apps if a.pass_fail == "Pass")
		self.save(ignore_permissions=True)
