"""Helper Functions"""

def doc_responses(error_codes):
    """Return responses dict for API docs"""
    responses = {
        200: "OK (Success)",
        201: "Created (Success)",
        204: "No Content (Success)",
        400: "Invalid Argument (Failed)",
        404: "Not Found (Failed)",
        405: "Wrong Method (Failed)",
        409: "Conflict or Duplicate (Failed)",
        415: "Unsupported Content Type (Failed)",
        500: "Internal Server Error (Failed)"
    }
    to_return = {}
    for ec in error_codes:
        if responses[ec]:
            to_return[ec] = responses[ec]
    return to_return
