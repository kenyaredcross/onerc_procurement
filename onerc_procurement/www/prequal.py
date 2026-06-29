import frappe

no_cache = 1


def get_context(context):
    context.boot = get_boot()
    return context


@frappe.whitelist(methods=["POST"], allow_guest=True)
def get_context_for_dev():
    if not frappe.conf.developer_mode:
        frappe.throw("This method is only for developer mode")
    return get_boot()


def get_boot():
    return frappe._dict(
        {
            "site_name": frappe.local.site,
            "csrf_token": frappe.sessions.get_csrf_token(),
            "frappe_version": frappe.__version__,
            "session_user": frappe.session.user,
            "user_email": frappe.session.user,
            "sysdefaults": frappe.defaults.get_defaults(),
        }
    )
