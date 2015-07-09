import datetime
from django.core.serializers.json import DjangoJSONEncoder
from .resources import Resource

class KnockoutEncoderMixin(object):

    def default(self, obj):
        try:
            if isinstance(obj, Resource):
                return obj.eval()
            elif isinstance(obj, datetime.timedelta):
                days = obj.days
                seconds = obj.seconds
                seconds += float(obj.microseconds)/1000000
                seconds += obj.days*24*60*60
                return '%d'%seconds
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return super(KnockoutEncoderMixin, self).default(obj)

class KnockoutEncoder(KnockoutEncoderMixin, DjangoJSONEncoder):
    pass
