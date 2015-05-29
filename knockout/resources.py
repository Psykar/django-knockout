def get_fields(fields, obj):
    obs_dict = {}
    for fld in fields:
        if isinstance(fld, (list, tuple)):
            fld, name = fld
        else:
            name = fld
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
        self.queryset = queryset

    def eval(self):
        objs = getattr(self, 'queryset', None)
        if objs is None:
            objs = self.model.objects.all()
        values = objs.values(*getattr(self, 'fields', []))
        extras = getattr(self, 'extras', None)
        if extras:
            for o, v in zip(objs, values):
                v.update(get_fields(extras, o))
        return values
