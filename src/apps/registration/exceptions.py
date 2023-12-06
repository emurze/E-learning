from django.core.exceptions import ValidationError


class RegistrationValidationError(ValidationError):
    pass
