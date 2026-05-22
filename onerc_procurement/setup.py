"""Post-install setup for onerc_procurement."""
import frappe
from frappe import _


_DEFAULT_SECTIONS = [
    ("Company Information", 10),
    ("Contact Details", 20),
    ("Banking Details", 30),
    ("Registration & Statutory", 40),
    ("Director / Shareholder Information", 50),
    ("Business Integrity", 60),
    ("Sustainable Procurement & ESG", 70),
    ("Governance & Compliance", 80),
    ("Trade References", 90),
    ("Financial Performance", 100),
    ("Declaration", 110),
]


def after_install():
    """Run once immediately after the app is installed on a site."""
    _create_organisation_settings()
    _create_default_question_sections()
    frappe.db.commit()


def _create_organisation_settings():
    if not frappe.db.exists("Organisation Settings", "Organisation Settings"):
        doc = frappe.new_doc("Organisation Settings")
        doc.organisation_name = "Kenya Red Cross Society"
        doc.default_fee = 5000
        doc.currency = "KES"
        doc.mpesa_environment = "sandbox"
        doc.s3_folder_prefix = "prequal"
        doc.insert(ignore_permissions=True)
        frappe.logger().info("onerc_procurement: Organisation Settings created")


def _create_default_question_sections():
    for section_name, order in _DEFAULT_SECTIONS:
        if not frappe.db.exists("Question Section", section_name):
            doc = frappe.new_doc("Question Section")
            doc.section_name = section_name
            doc.order = order
            doc.is_mandatory_for_all = 1
            doc.applies_to_supplier_portal = 1
            doc.insert(ignore_permissions=True)
            frappe.logger().info(f"onerc_procurement: Created Question Section '{section_name}'")
