"""Utility helpers for the onerc_procurement app."""
import frappe
from frappe.utils import now_datetime


def generate_application_code(exercise, category, supplier):
    """Generate a human-readable reference combining exercise, category and supplier codes."""
    return f"{exercise}/{category}/{supplier}"


def format_kes(amount):
    """Format a number as a KES currency string."""
    if amount is None:
        return "KES 0.00"
    return f"KES {float(amount):,.2f}"


def is_within_edit_window(application):
    """Check whether a Prequal Application can still be edited."""
    if isinstance(application, str):
        application = frappe.get_doc("Prequal Application", application)
    return application.is_editable()


def send_notification(recipient, subject, message, template=None):
    """Send an email notification to a recipient."""
    frappe.sendmail(
        recipients=[recipient],
        subject=subject,
        message=message,
        now=True,
    )
