from simplejson import JSONEncoder
from .resources import Resource

class KnockoutEncoderMixin(object):

    def default(self, obj):
        try:
            if isinstance(obj, Resource):
                return obj.eval()
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return super(KnockoutEncoderMixin, self).default(obj)

class KnockoutEncoder(KnockoutEncoderMixin, JSONEncoder):
    pass
