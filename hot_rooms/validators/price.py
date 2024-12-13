from django.core.exceptions import ValidationError

def validate_positive(value):
    if value < 0:
        raise ValidationError('Value must be a positive integer.')
