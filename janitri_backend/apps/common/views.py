from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from utils.constants.choices import CHOICES_MAP
from utils.responses import success_response, error_response
from drf_spectacular.utils import extend_schema, OpenApiParameter
from enum import Enum

class ChoiceTypeEnum(str, Enum):
    role = "role"
    gender = "gender"
    relation = "relation"

@extend_schema(
    parameters=[
        OpenApiParameter(
            name="type",
            description="Select choice type(s) to filter",
            required=False,
            type=str,
            enum=[e.value for e in ChoiceTypeEnum],  # dropdown in Swagger
        )
    ],
    responses={200: dict, 400: dict}  # generic dict, no serializer needed
)
@api_view(["GET"])
def choices_view(request):
    """
    Return filtered choice fields for frontend.
    Use query param 'type' to filter: ?type=role,gender
    """
    try:
        types_param = request.query_params.get("type")
        if types_param:
            requested_types = [t.strip() for t in types_param.split(",")]
        else:
            requested_types = CHOICES_MAP.keys()

        data = {}
        for choice_type in requested_types:
            choices = CHOICES_MAP.get(choice_type)
            if choices:
                data[f"{choice_type}_choices"] = [{"key": k, "value": v} for k, v in choices]

        return success_response(message="Choices fetched successfully", data=data)
    
    except Exception as e:
        return error_response(message="Failed to fetch choices", errors=str(e), status=500)
