from kris_models import ProjectInvitation


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
