from rest_framework import permissions

from api.models import Projects, Issues, Contributors, Comments

class ProjectsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated and Projects.objects.filter(contributors__user=request.user, id=view.kwargs.get('project_id')).exists()
        else:
            return request.user.is_authenticated and Projects.objects.filter(author=request.user, id=view.kwargs.get('project_id')).exists()

