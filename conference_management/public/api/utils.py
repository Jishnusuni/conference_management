import frappe
from frappe.utils import now

def log_api_request(api_endpoint, method="GET", request_body=None, response_body=None, status_code=200):
    """
    Logs API requests and responses to the API Log doctype.

    Args:
        api_endpoint (str): API endpoint name
        method (str): HTTP method (GET, POST, PUT, DELETE)
        request_body (dict/str): Input data
        response_body (dict/str): API response
        status_code (int): Response HTTP status code
    """
    try:
        frappe.get_doc({
            "doctype": "API Log",
            "api_endpoint": api_endpoint,
            "method": method,
            "request_body": str(request_body) if request_body else "",
            "response_body": str(response_body) if response_body else "",
            "status_code": status_code
        }).insert(ignore_permissions=True)
    except Exception as e:
        # Fail silently so logging doesn't break the API
        frappe.log_error(frappe.get_traceback(), "API Logging Error")
