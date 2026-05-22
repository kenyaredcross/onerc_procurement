import json
import frappe
from frappe import _
from frappe.model.document import Document

_DEFAULT_RUBRICS = {
	"Tiered": {"type": "tiered", "tiers": [{"label": "Excellent", "points": 10}, {"label": "Good", "points": 7}, {"label": "Average", "points": 5}, {"label": "Poor", "points": 0}]},
	"Yes-No Binary": {"type": "yesno", "yes_points": 10, "no_points": 0},
	"Presence Check": {"type": "presence", "present_points": 10, "absent_points": 0},
	"Numeric Range": {"type": "numeric_range", "ranges": [{"min": 10, "max": None, "label": "10+", "points": 10}, {"min": 5, "max": 9, "label": "5-9", "points": 7}, {"min": 0, "max": 4, "label": "0-4", "points": 3}]},
}


class Question(Document):
	def validate(self):
		if self.is_scoreable and self.scoring_type and self.scoring_type != "Manual":
			if not self.scoring_rubric:
				default = _DEFAULT_RUBRICS.get(self.scoring_type)
				if default:
					self.scoring_rubric = json.dumps(default, indent=2)
			if self.scoring_rubric:
				try:
					json.loads(self.scoring_rubric)
				except (json.JSONDecodeError, ValueError):
					frappe.throw(_("Scoring Rubric must be valid JSON"))

	def suggest_score(self, response_value):
		"""Returns (suggested_score, label) tuple or (None, None) for Manual/Tiered."""
		if not self.is_scoreable or not self.scoring_type or self.scoring_type in ("Manual", "Tiered"):
			return None, None
		if not self.scoring_rubric:
			return None, None

		try:
			rubric = json.loads(self.scoring_rubric)
		except (json.JSONDecodeError, ValueError):
			return None, None

		rtype = rubric.get("type")

		if rtype == "presence":
			if response_value:
				return rubric.get("present_points", 0), "Present"
			return rubric.get("absent_points", 0), "Absent"

		if rtype == "yesno":
			val = str(response_value).strip().lower()
			if val in ("yes", "1", "true"):
				return rubric.get("yes_points", 0), "Yes"
			return rubric.get("no_points", 0), "No"

		if rtype == "numeric_range":
			try:
				num = float(response_value)
			except (TypeError, ValueError):
				return None, None
			for r in rubric.get("ranges", []):
				lo = r.get("min")
				hi = r.get("max")
				if (lo is None or num >= lo) and (hi is None or num <= hi):
					return r.get("points", 0), r.get("label", "")
			return 0, "Outside defined ranges"

		return None, None
