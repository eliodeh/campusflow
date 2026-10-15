class ValidationError(Exception):
    """Raised when a value fails validation."""


def validate_affected_users(value):
    if isinstance(value, bool):          
       raise ValidationError("affected_users must be an integer, not a boolean")
    if not isinstance(value, int):      
        raise ValidationError("affected_users must be an integer")
    if value <= 0:                      
        raise ValidationError("affected_users must be greater than zero")
    return value

def validate_title(value):
    if not isinstance(value, str):
        raise ValidationError("title must be a string")
    if not value.strip():
        raise ValidationError("title cannot be blank")
    return value.strip()