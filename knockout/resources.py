def get_fields(fields, obj):
    obs_dict = {}
    for fld in fields:
        if isinstance(fld, (list, tuple)):
            fld, name = fld
        else:
            name = fld
        if callable(fld):
            val = fld(obj)
        else:
            links = fld.split('__')
            val = obj
            for lnk in links:
                val = getattr(val, lnk)
                if callable(val):
                    val = val()
        obs_dict[name] = val
    return obs_dict

class Resource(object):

    def __init__(self, queryset=None):
        if queryset is not None:
            self.queryset = queryset
        # Copy the class queryset so any cached results are reset.
        self.queryset = self.queryset.all()

    def eval(self):

        # Were we given something?
        objs = getattr(self, 'queryset', None)
        if objs is None:
            objs = self.model.objects.all()

        # Is it a queryset, or an object?
        if not isinstance(objs, self.model):
            values = objs.values(*getattr(self, 'fields', []))
            extras = getattr(self, 'extras', None)
            if extras:
                for o, v in zip(objs, values):
                    v.update(get_fields(extras, o))
        else:
            values = {}
            for field in getattr(self, 'fields', []):
                values[field] = getattr(objs, field, None)

        return values
