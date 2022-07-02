# -*- coding: utf-8 -*-

from django.core.exceptions import ValidationError
from django.utils import timezone


def yamdb_year_validator(value):
    if value > timezone.now().year:
        raise ValidationError(f'{value} is not a valid year!')
