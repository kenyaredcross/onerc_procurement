"""M-Pesa Daraja STK Push integration stubs."""
import frappe
from frappe import _


@frappe.whitelist()
def initiate_stk_push(supplier, exercise, categories, phone_number):
    """Initiate M-Pesa STK Push for a supplier application payment.

    Args:
        supplier: Supplier Profile name
        exercise: Prequal Exercise name
        categories: JSON list of Prequal Category names
        phone_number: Safaricom phone number (2547xxxxxxxx format)

    Returns:
        dict with checkout_request_id and payment_transaction name
    """
    # TODO Phase 2: implement Daraja STK Push
    frappe.throw(_("Payment processing not yet implemented"))


@frappe.whitelist(allow_guest=True)
def mpesa_callback(data=None):
    """Receive M-Pesa STK callback from Safaricom Daraja.

    This endpoint must be publicly accessible (allow_guest=True).
    Safaricom posts JSON to this URL after STK Push completes.
    """
    # TODO Phase 2: parse callback, update Payment Transaction, unlock applications
    pass


def check_pending_payments():
    """Scheduler task — hourly.

    Query Payment Transactions stuck in Pending/Initiated for more than
    10 minutes and attempt to reconcile via Daraja query API.
    """
    # TODO Phase 2: implement stale payment reconciliation
    pass


def get_daraja_token():
    """Fetch a fresh OAuth2 bearer token from Safaricom Daraja.

    Returns:
        str: access_token
    """
    # TODO Phase 2: implement token fetch with caching
    pass
