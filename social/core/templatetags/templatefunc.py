from django import template
from core.path_utils import get_post_id_from_url

register = template.Library()

@register.simple_tag
def urltoid(value):
    return get_post_id_from_url(value)