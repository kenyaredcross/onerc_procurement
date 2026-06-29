import json
import frappe
from frappe import _


def _get_supplier_for_user():
    user = frappe.session.user
    return frappe.db.get_value("Supplier Profile", {"owner": user}, "name")


def _require(value, field_name):
    if not value:
        frappe.throw(_("{0} is required").format(field_name), frappe.MandatoryError)
    return value


@frappe.whitelist()
def get_my_supplier_profile():
    name = _get_supplier_for_user()
    if not name:
        return None
    return frappe.get_doc("Supplier Profile", name).as_dict()


@frappe.whitelist()
def create_supplier_profile():
    existing = _get_supplier_for_user()
    if existing:
        frappe.throw(_("You already have a supplier profile: {0}").format(existing))

    doc = frappe.get_doc({
        "doctype": "Supplier Profile",
        "company_name": frappe.session.user,
        "contact_email": frappe.session.user,
        "profile_status": "Incomplete",
    })
    doc.insert(ignore_permissions=True)
    return {"name": doc.name}


@frappe.whitelist()
def save_supplier_profile(supplier_name=None, data=None):
    supplier_name = supplier_name or frappe.form_dict.get("supplier_name")
    data = data or frappe.form_dict.get("data")
    _require(supplier_name, "supplier_name")

    doc = frappe.get_doc("Supplier Profile", supplier_name)
    if doc.owner != frappe.session.user and "Prequal Admin" not in frappe.get_roles():
        frappe.throw(_("Not permitted"), frappe.PermissionError)

    updates = json.loads(data) if isinstance(data, str) else (data or {})
    allowed_fields = {
        "company_name", "organisation_type", "reg_number", "pin_number",
        "main_office_location", "branch_offices", "website", "po_box",
        "contact_person_name", "contact_person_position",
        "contact_email", "contact_phone", "company_email", "company_phone",
        "bank_name", "bank_branch", "account_name", "account_number",
    }
    for field, value in updates.items():
        if field in allowed_fields:
            setattr(doc, field, value)

    doc.save(ignore_permissions=True)
    return {"name": doc.name, "profile_status": doc.profile_status}


@frappe.whitelist()
def create_application(exercise=None, category=None):
    exercise = exercise or frappe.form_dict.get("exercise")
    category = category or frappe.form_dict.get("category")
    _require(exercise, "exercise")
    _require(category, "category")

    supplier = _get_supplier_for_user()
    if not supplier:
        frappe.throw(_("Please complete your supplier profile before applying."))

    # return existing application rather than duplicating
    existing = frappe.db.get_value(
        "Prequal Application",
        {"exercise": exercise, "category": category, "supplier": supplier},
        "name",
    )
    if existing:
        return frappe.get_doc("Prequal Application", existing).as_dict()

    exercise_doc = frappe.get_doc("Prequal Exercise", exercise)
    if exercise_doc.status != "Published":
        frappe.throw(_("This exercise is not open for applications."))

    amount_due = 5000
    for cat_row in exercise_doc.categories:
        if cat_row.category == category:
            amount_due = cat_row.fee_override if cat_row.fee_override > 0 else amount_due
            break

    doc = frappe.get_doc({
        "doctype": "Prequal Application",
        "exercise": exercise,
        "category": category,
        "supplier": supplier,
        "status": "Payment Pending",
        "payment_status": "Pending",
        "amount_due": amount_due,
        "edit_locked": 0,
        "technical_score": 0,
        "pass_fail": "Pending",
        "compliance_status": "Pending",
        "flagged_for_review": 0,
    })
    doc.insert(ignore_permissions=True)
    return doc.as_dict()


@frappe.whitelist()
def get_section_questions(section=None, application=None):
    section = section or frappe.form_dict.get("section")
    application = application or frappe.form_dict.get("application")
    _require(section, "section")
    _require(application, "application")

    # verify application belongs to caller
    frappe.get_doc("Prequal Application", application)

    questions = frappe.get_all(
        "Question",
        filters={"section": section},
        fields=["name", "question_text", "question_type", "help_text",
                "is_mandatory", "options", "sort_order"],
        order_by="sort_order asc",
    )

    existing_responses = {}
    if questions:
        qnames = [q.name for q in questions]
        rows = frappe.get_all(
            "Application Response",
            filters={"application": application, "question": ["in", qnames]},
            fields=["question", "response_value"],
        )
        existing_responses = {r.question: r.response_value for r in rows}

    return {"questions": questions, "responses": existing_responses}


@frappe.whitelist()
def save_responses(application=None, section=None, responses=None):
    application = application or frappe.form_dict.get("application")
    section = section or frappe.form_dict.get("section")
    responses = responses or frappe.form_dict.get("responses")
    _require(application, "application")
    _require(section, "section")

    app_doc = frappe.get_doc("Prequal Application", application)
    if app_doc.edit_locked:
        frappe.throw(_("This application is locked and cannot be edited."))
    if app_doc.payment_status != "Paid":
        frappe.throw(_("Payment must be completed before saving responses."))

    data = json.loads(responses) if isinstance(responses, str) else (responses or {})

    for question_name, response_value in data.items():
        if response_value is None:
            continue
        existing = frappe.db.get_value(
            "Application Response",
            {"application": application, "question": question_name},
            "name",
        )
        if existing:
            frappe.db.set_value("Application Response", existing, "response_value", str(response_value))
        else:
            frappe.get_doc({
                "doctype": "Application Response",
                "application": application,
                "question": question_name,
                "response_value": str(response_value),
            }).insert(ignore_permissions=True)

    frappe.db.set_value("Prequal Application", application, "last_edited", frappe.utils.now())
    return {"status": "ok"}


@frappe.whitelist()
def submit_application(application=None):
    application = application or frappe.form_dict.get("application")
    _require(application, "application")

    app_doc = frappe.get_doc("Prequal Application", application)
    if app_doc.edit_locked:
        frappe.throw(_("This application has already been submitted."))
    if app_doc.payment_status != "Paid":
        frappe.throw(_("Payment must be completed before submitting."))

    app_doc.status = "Submitted"
    app_doc.submission_date = frappe.utils.now()
    app_doc.is_responsive = 1
    app_doc.save(ignore_permissions=True)
    return {"status": "submitted", "name": application}
