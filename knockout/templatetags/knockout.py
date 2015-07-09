import json
from django.template import Library
from django.utils.html import escapejs
from django.utils.safestring import mark_safe
from ..serial import KnockoutEncoder

register = Library()

@register.filter(is_safe=True)
def knockout(value, name='data'):
    data = escapejs(json.dumps(value, cls=KnockoutEncoder))
    return mark_safe('%s = "%s";'%(name, data))
