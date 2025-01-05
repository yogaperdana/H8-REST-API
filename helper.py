"""Helper Functions"""
import json
from flask import Response

def doc_responses(error_codes: list[int]) -> dict[int, str]:
    """Generate responses dictionary for API docs"""
    responses = {
        200: "OK",
        201: "Created",
        204: "No Content",
        400: "Invalid Argument",
        401: "Authorization Failed",
        404: "Not Found",
        405: "Wrong Method",
        409: "Conflict or Duplicate",
        415: "Unsupported Content Type",
        500: "Internal Server Error"
    }
    to_return = {}
    for ec in error_codes:
        if responses[ec]:
            to_return[ec] = responses[ec]
    return to_return

def response_json(response: dict[str, str], status: int = 200) -> Response:
    """Generate response as JSON"""
    return Response(json.dumps(response), status, content_type="application/json")

def response_none(status: int) -> Response:
    """Generate an empty response"""
    return Response(None, status, content_type="application/json")
