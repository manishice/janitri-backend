from django.core.validators import RegexValidator
phone_validator = RegexValidator(
    regex=r'^\d{10}$',
    message="Phone number must be exactly 10 digits."
)