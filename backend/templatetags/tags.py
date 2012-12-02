from django import template
from backend.forms import searchForm
import os

register = template.Library()

@register.inclusion_tag('/lookup.html')
def lookup():
  return {'searchForm': searchForm()}
