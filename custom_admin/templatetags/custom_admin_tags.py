from django import template

register = template.Library()


@register.simple_tag(takes_context=True)
def active_link(context, url_prefix):
    request = context.get('request')
    if request:
        resolver_match = request.resolver_match
        if resolver_match and resolver_match.url_name and resolver_match.url_name.startswith(url_prefix):
            return 'active'
    return ''
