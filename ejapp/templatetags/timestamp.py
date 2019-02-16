import datetime as datetime
from django import template
from datetime import datetime

register = template.Library()

@register.filter(name='change')
def change(value, arg):
    """Removes all values of arg from the given string"""
    date_time = datetime.fromtimestamp(int(value))
    if arg == "date":
        ret = date_time.date()
    else:
        ret = date_time.time()
    return ret
