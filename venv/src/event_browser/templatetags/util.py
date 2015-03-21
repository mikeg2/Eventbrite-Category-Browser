from django import template

register = template.Library()

@register.filter(name="range")
def get_range(count):
    return range(int(count))

@register.simple_tag
def url_replace(request, *args):
    editable_get = request.GET.copy()
    for i in xrange(0, len(args), 2):
        field = args[i]
        value = args[i+1]
        editable_get[field] = value
    return editable_get.urlencode()

@register.filter
def index(array, index):
    return array[int(index)]