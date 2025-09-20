from rest_framework.response import Response

SUCCESS = "success"
ERROR = "error"


def success_response(message="Success", data=None, status=200):
    response_data = {
            "status": SUCCESS,
            "message": message
        }

    if data is not None:
        response_data["data"] = data
    return Response(
        response_data,
        status=status
    )


def error_response(message="Something went wrong", errors=None, status=400):
    return Response(
        {
            "status": ERROR,
            "message": message,
            "errors": errors if errors else {},
        },
        status=status,
    )
