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
    queryset = None

    def __init__(self, queryset=None):
        if queryset is not None:
            self.queryset = queryset

        if self.queryset is None:
            self.queryset = self.model.objects

    def eval(self):
        # Copy the queryset so any cached results are reset.
        objs = self.queryset.all()
        fields = getattr(self, 'fields', [])
        annotations = getattr(self, 'annotations', [])

        for (annotation, method, field) in annotations:
            objs = objs.annotate(**{
                annotation: method(field)
            })
            fields.append(annotation)

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
