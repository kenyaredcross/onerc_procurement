import frappe
from frappe import _
from frappe.model.document import Document
from frappe.utils import now_datetime


class ScoreSheet(Document):
	def before_submit(self):
		if self.mandatory_check not in ("Pass", "Fail"):
			frappe.throw(_("Mandatory Check must be set to Pass or Fail before submitting"))
		for row in self.score_lines:
			if row.final_score is None:
				frappe.throw(_("All score lines must have a Final Score before submitting"))

	def on_submit(self):
		self._compute_total_score()
		self._determine_pass_fail()
		self._set_panel_summary()
		self._update_application()

	def _compute_total_score(self):
		self.total_score = sum(row.final_score or 0 for row in self.score_lines)

	def _determine_pass_fail(self):
		if not self.application:
			return
		app = frappe.get_doc("Prequal Application", self.application)
		category = frappe.get_doc("Prequal Category", app.category)
		pass_mark = category.pass_mark or 60
		max_score = category.max_score or 100
		pct = (self.total_score / max_score) * 100 if max_score else 0
		self.pass_fail = "Pass" if pct >= pass_mark else "Fail"

	def _set_panel_summary(self):
		self.evaluated_by = frappe.session.user
		self.evaluation_date = now_datetime()
		if self.panel:
			panel = frappe.get_doc("Evaluation Panel", self.panel)
			member_names = [m.full_name or m.user for m in panel.members if m.role == "Member"]
			lead = panel.lead_evaluator
			self.panel_members_summary = f"Lead: {lead}. Panel: {', '.join(member_names)}"

	def _update_application(self):
		if not self.application:
			return
		app = frappe.get_doc("Prequal Application", self.application)
		app.technical_score = self.total_score
		app.pass_fail = self.pass_fail
		app.status = "Evaluated"
		app.save(ignore_permissions=True)
