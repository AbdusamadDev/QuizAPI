from django.core.exceptions import ValidationError


def validate_answer_number(value):
    if not 1 <= value <= 4:
        raise ValidationError('You can write only from 1 to 4 numbers.')