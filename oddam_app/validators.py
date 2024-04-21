import re

from django.core.exceptions import ValidationError


class SpecialCharValidator(object):
    '''PASSWORD MUST CONTAINS ONE UPPER CASE,ONE LOWER CASE, ONE NUMBER, ONE SPECIAL CHARACTER'''

    def validate(self, password, user=None):
        specials = r'[!@#$%^&*()_+\-=\[\]{};:\'"\\|,.<>\/?]'
        if not re.search(specials, password):
            raise ValidationError('Hasło musi zawierac znak specjalny.')

    def get_help_text(self):
        return (
            'Hasło musi zawierać znak specjalny, małą litere, wielką literę oraz cyfrę'
        )


class LowerCharValidator(object):
    def validate(self, password,user=None):
        if not re.search(r'[a-z]', password):
            raise ValidationError('Hasło musi zawierac  małą litere.')

    def get_help_text(self):
        return (
            'Hasło musi zawierać znak specjalny, małą litere, wielką literę oraz cyfrę'
        )


class UpperCharValidator(object):
    def validate(self, password,user=None):
        if not re.search(r'[A-Z]', password):
            raise ValidationError('Hasło musi zawierac wielka litere.')

    def get_help_text(self):
        return (
            'Hasło musi zawierać znak specjalny, małą litere, wielką literę oraz cyfrę'
        )


class DigitCharValidator(object):
    def validate(self, password,user=None):
        if not re.search(r'\d', password):
            raise ValidationError('Hasło musi zawierac cyfre.')

    def get_help_text(self):
        return (
            'Hasło musi zawierać znak specjalny, małą litere, wielką literę oraz cyfrę'
        )
