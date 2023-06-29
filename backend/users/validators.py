import datetime
import re
from django.core.exceptions import ValidationError

# Custom validation function for username
def validate_username(value):
    if not bool(re.match(r'^[\w.@+-]+$', value)):
        raise ValidationError(
            'Incorrect symbols in username'
        )
    return value


# Custom validation function for year
def validate_year(year):
    this_year = datetime.date.today().year
    if year > this_year:
        raise ValidationError(
            'It`s not possible now'
        )
