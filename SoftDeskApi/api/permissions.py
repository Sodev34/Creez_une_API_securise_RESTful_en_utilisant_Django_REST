from rest_framework import permissions

from api.models import Projects, Issues, Comments


class ProjectsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            project_id = view.kwargs.get("project_id")
            if request.method in permissions.SAFE_METHODS:
                return Projects.objects.filter(contributors__user=request.user)
            return request.user == project_id.author
        except (KeyError, Projects.DoesNotExist):
            return True


class ContributorsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")
        if request.method in permissions.SAFE_METHODS:
            return (
                request.user.is_authenticated
                and Projects.objects.filter(
                    contributors__user=request.user, id=project_id
                ).exists()
            )
        else:
            return (
                request.user.is_authenticated
                and Projects.objects.filter(author=request.user, id=project_id).exists()
            )


class IssuesPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        try:
            issue_id = view.kwargs.get("issue_id")
            issue = Issues.objects.get(id=issue_id)
            return request.user == issue.author
        except Issues.DoesNotExist:
            project_id = view.kwargs.get("project_id")
            project = Projects.objects.get(id=project_id)
            return request.user.is_authenticated and project in Projects.objects.filter(
                contributors__user=request.user
            )


class CommentsPermissions(permissions.BasePermission):
    def has_permission(self, request, view):
        project_id = view.kwargs.get("project_id")
        try:
            comment_id = view.kwargs.get("comment_id")
            comment = Comments.objects.get(id=comment_id)
            if request.method in permissions.SAFE_METHODS:
                return Projects.objects.filter(
                    contributors__user=request.user, id=project_id
                ).exists()
            return request.user == comment.author
        except Comments.DoesNotExist:
            project = Projects.objects.get(id=project_id)
            return request.user.is_authenticated and project in Projects.objects.filter(
                contributors__user=request.user
            )
