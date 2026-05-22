"""Evaluation API stubs."""
import frappe


def on_score_submit(doc, method):
    """doc_event hook — called after Score Sheet is submitted.

    The Score Sheet controller already handles updating the application.
    This hook is reserved for additional side-effects such as:
    - notifying the supplier
    - triggering audit logs
    - updating exercise statistics
    """
    # TODO Phase 2: add notifications and statistics update
    pass


@frappe.whitelist()
def get_application_with_scores(application_name):
    """Return application details together with all Score Sheets and score lines.

    Args:
        application_name: Prequal Application name

    Returns:
        dict with application fields and nested score sheets
    """
    # TODO Phase 2: implement
    frappe.throw(frappe._("Not yet implemented"))


@frappe.whitelist()
def get_suggested_scores(application_name):
    """Pre-compute suggested scores for all scoreable questions in an application.

    Called by the evaluation workspace to pre-populate Score Lines.

    Args:
        application_name: Prequal Application name

    Returns:
        list of dicts: [{question, criterion_label, max_score, suggested_score, suggested_label}]
    """
    # TODO Phase 2: implement
    frappe.throw(frappe._("Not yet implemented"))
