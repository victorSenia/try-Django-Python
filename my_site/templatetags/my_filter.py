from django import template

register = template.Library()


@register.filter("add_class")
def add_class(value, clazz):
    if hasattr(value, "field"):
        add_clas(value.field.widget.attrs, clazz)
    elif hasattr(value, "fields"):
        for name, field in value.fields.items():
            add_clas(field.widget.attrs, clazz)
    return value


def add_clas(attrs, clazz):
    c = attrs.get("class")
    if c:
        c += " " + clazz
    else:
        c = clazz
    attrs['class'] = c
    return attrs


@register.filter("contain_key")
def contain_key(dic, key):
    return dic.get(key)


@register.filter("get_key")
def get_key(dic, key):
    return dic.get(key)


@register.filter("get_type")
def get_key(field):
    return str(type(field))
