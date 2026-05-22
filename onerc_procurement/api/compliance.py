"""Compliance API stubs."""
import frappe


def on_compliance_submit(doc, method):
    """doc_event hook — called after Compliance Record is submitted.

    The Compliance Record controller handles updating the application status.
    This hook is reserved for:
    - notifications to the compliance officer / admin
    - audit trail entries
    """
    # TODO Phase 2: add notifications
    pass


@frappe.whitelist()
def build_compliance_record(application_name):
    """Auto-build a Compliance Record pre-populated from the category checklist.

    Reads the Prequal Category.compliance_checklist for the application's
    category and creates a draft Compliance Record with matching Compliance Items.

    Args:
        application_name: Prequal Application name

    Returns:
        str: new Compliance Record name
    """
    # TODO Phase 2: implement
    frappe.throw(frappe._("Not yet implemented"))
