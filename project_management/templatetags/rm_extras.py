from django import template
from rango.models import Project

register = template.Library()

@register.inclusion_tag('project_management/project_list.html')
def get_project_list(current_project=None):
    return {'user_projects': Project.objects.all(), 'acting_project': current_project}
