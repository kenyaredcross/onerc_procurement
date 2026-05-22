"""AWS S3 file management stubs."""
import frappe
from frappe import _


def upload_file(file_content, filename, supplier_id, application_id=None):
    """Upload a file to S3 and return the S3 key.

    Args:
        file_content: bytes — file data
        filename: str — original filename
        supplier_id: str — Supplier Profile name (used for folder path)
        application_id: str — Prequal Application name (optional subfolder)

    Returns:
        str: S3 key of the uploaded file
    """
    # TODO Phase 2: implement boto3 upload using Organisation Settings credentials
    frappe.throw(_("S3 upload not yet implemented"))


def get_presigned_url(s3_key, expiry_seconds=3600):
    """Generate a pre-signed URL for secure time-limited access to an S3 object.

    Args:
        s3_key: str — S3 object key
        expiry_seconds: int — URL validity in seconds (default 1 hour)

    Returns:
        str: pre-signed URL
    """
    # TODO Phase 2: implement boto3 generate_presigned_url
    frappe.throw(_("S3 pre-signed URL not yet implemented"))


def delete_file(s3_key):
    """Delete an object from S3.

    Args:
        s3_key: str — S3 object key

    Returns:
        bool: True if deleted successfully
    """
    # TODO Phase 2: implement boto3 delete_object
    frappe.throw(_("S3 delete not yet implemented"))
