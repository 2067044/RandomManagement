from django.contrib.auth.decorators import login_required
from kris_models import ProjectInvitation
from project_management.views import getUserProjects, getAdminProjects, getMemberProjects


def user_invitations(request):
    '''This method ensures that every single template will have access
    to the current logged in user's project invitations.
    :param request:
    :return:
    '''
    project_invitations = None
    if request.user.is_authenticated():
        project_invitations = ProjectInvitation.objects.filter(user=request.user)
    return {'project_invitations': project_invitations}

def all_user_projects(request):
    user_projects = None
    member_projects = None
    admin_projects = None
    if request.user.is_authenticated():
        user_projects = getUserProjects(request.user)
        member_projects = getMemberProjects(request.user)
        admin_projects = getAdminProjects(request.user)
    return {'user_projects':user_projects, 'member_projects':member_projects, 'admin_projects': admin_projects}

