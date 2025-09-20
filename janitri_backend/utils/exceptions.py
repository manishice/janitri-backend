from rest_framework.views import exception_handler
from .responses import error_response


def custom_exception_handler(exc, context):
    # First call DRF's default exception handler
    response = exception_handler(exc, context)

    if response is not None:
        # Authentication/permission errors
        if response.status_code == 401:
            return error_response(
                message="Authentication credentials were not provided or invalid",
                status=401,
            )
        elif response.status_code == 403:
            return error_response(
                message="You do not have permission to perform this action",
                status=403,
            )

        # Validation / other DRF errors
        return error_response(
            message=response.data.get("detail", "An error occurred"),
            errors=response.data,
            status=response.status_code,
        )

    # If DRF could not handle it
    return error_response(
        message="Internal server error",
        status=500,
    )
