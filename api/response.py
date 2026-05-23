from rest_framework.response import Response
from rest_framework.views import exception_handler

SUCCESS_CODE = "00"
ERROR_CODE = "99"
PENDING_CODE = "01"


def api_response(message, data=None, status_code=200, status=SUCCESS_CODE):
    return Response(
        {
            "status": status,
            "message": message,
            "data": {} if data is None else data,
        },
        status=status_code,
    )


def success_response(message, data=None, status_code=200):
    return api_response(message, data=data, status_code=status_code, status=SUCCESS_CODE)


def error_response(message, data=None, status_code=400):
    return api_response(message, data=data, status_code=status_code, status=ERROR_CODE)


def pending_response(message, data=None, status_code=202):
    return api_response(message, data=data, status_code=status_code, status=PENDING_CODE)


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is None:
        return None

    detail = response.data
    message = "Request failed"

    if isinstance(detail, dict):
        if "detail" in detail:
            message = str(detail["detail"])
        elif detail:
            message = "Validation error"
    elif isinstance(detail, list):
        message = "Validation error"
    elif detail:
        message = str(detail)

    response.data = {
        "status": ERROR_CODE,
        "message": message,
        "data": detail,
    }
    return response
