import frappe
from frappe.model.document import Document


class ApplicationResponse(Document):
	def before_save(self):
		if self.question:
			q = frappe.get_doc("Question", self.question)
			self.question_text = q.question_text
			self.question_type = q.question_type

			response_value = self._get_response_value(q.question_type)
			score, label = q.suggest_score(response_value)
			if score is not None:
				self.suggested_score = score
				self.suggested_score_label = label or ""

	def _get_response_value(self, question_type):
		if question_type in ("Text", "Long Text", "Declaration"):
			return self.text_response
		if question_type in ("Number", "Currency (KES)"):
			return self.number_response
		if question_type == "Yes-No":
			return "Yes" if self.boolean_response else "No"
		if question_type == "File Upload":
			return self.file_response
		if question_type == "Date":
			return self.date_response
		return self.text_response
