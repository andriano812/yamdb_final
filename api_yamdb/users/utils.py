# -*- coding: utf-8 -*-

from django.core import mail
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from api_yamdb.settings import NOREPLY_EMAIL


def email_is_valid(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def generate_mail(email, code):
    subject = 'YamDB confirmation code'
    to = email
    text = f'Your confirmation code for YamDB: {code}'
    mail.send_mail(
        subject, text,
        NOREPLY_EMAIL, [to],
        fail_silently=False
    )
