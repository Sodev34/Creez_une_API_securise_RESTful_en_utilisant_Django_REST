from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework.views import APIView

from api.models import Projects, Contributors, Issues, Comments

from .permissions import (
    ProjectsPermissions,
    ContributorsPermissions,
    IssuesPermissions,
    CommentsPermissions,
)

from api.serializers import (
    ProjectsSerializer,
    IssuesSerializer,
    CommentsSerializer,
    ContributorsSerializer,
)

class ProjectListView(APIView):
    permission_classes = [IsAuthenticated, ProjectsPermissions]

    def get(self, request):
        projects = Projects.objects.filter(contributors__user=request.user)

        serializer = ProjectsSerializer(projects, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        data = request.data.copy()
        data['author'] = request.user.id

        serializer = ProjectsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            project = serializer.save()
            Contributors.objects.create(user=request.user, project=project, role='author')
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class ProjectDetailView(APIView):
    permission_classes = [IsAuthenticated, ProjectsPermissions]

    def get(self, request, project_id):
        project = get_object_or_404(Projects, id=project_id)
        serializer = ProjectsSerializer(project)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id):
        project = get_object_or_404(Projects, id=project_id)
        data = request.data.copy()
        data['author'] = project.author.id

        serializer = ProjectsSerializer(project, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id):
        project = get_object_or_404(Projects, id=project_id)
        project.delete()
        return Response('Projet supprimé avec succès.', status=status.HTTP_204_NO_CONTENT)
    
class ContributorListView(APIView):
    permission_classes = [IsAuthenticated, ContributorsPermissions]

    def get(self, request, project_id):
        project = get_object_or_404(Projects, id=project_id)
        contributors = Contributors.objects.filter(project=project)
        serializer = ContributorsSerializer(contributors, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id):
        project = get_object_or_404(Projects, id=project_id)
        data = request.data.copy()
        data['project'] = project.id
        #print(data)

        try:
            Contributors.objects.get(user=data['user'], project=project.id)
            return Response('Cet utilisateur a déjà été ajouté en tant que contributeur à ce projet.', status=status.HTTP_400_BAD_REQUEST)
        except Contributors.DoesNotExist:
            try:
                User.objects.get(id=data['user'])
                serializer = ContributorsSerializer(data=data)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            except User.DoesNotExist:
                return Response("L'Utilisateur n'existe pas.", status=status.HTTP_400_BAD_REQUEST)
            
class DeleteContributorView(APIView):
    permission_classes = [IsAuthenticated, ContributorsPermissions]

    def delete(self, request, project_id, user_id):
        get_object_or_404(Projects, id=project_id)
        contributor = get_object_or_404(Contributors, id=user_id)

        if contributor.role == 'author':
            return Response("L'auteur du projet ne peut pas être supprimé", status=status.HTTP_400_BAD_REQUEST)
        else:
            contributor.delete()
            return Response("Contributeur supprimé avec succès.", status=status.HTTP_204_NO_CONTENT)


class IssueListView(APIView):
    permission_classes = [IsAuthenticated, IssuesPermissions]

    def get(self, request, project_id):
        project = get_object_or_404(Projects, id=project_id)
        issues = Issues.objects.filter(project=project)
        serializer = IssuesSerializer(issues, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
    
    def post(self, request, project_id):
        project = get_object_or_404(Projects, id=project_id)
        data = request.data.copy()
        data['project'] = project.id
        data['author'] = request.user.id
        #print(data)

        try:
            Contributors.objects.get(id=data['assignee'], project=project.id)
            serializer = IssuesSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
        except Contributors.DoesNotExist:
            return Response(
                "Cet utilisateur n'existe pas.",
                status=status.HTTP_400_BAD_REQUEST
            )
        
class IssueDetailView(APIView):
    permission_classes = [IsAuthenticated, IssuesPermissions]

    def get(self, request, project_id, issue_id):
        issue = get_object_or_404(Issues, id=issue_id)
        serializer = IssuesSerializer(issue)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id, issue_id):
        project = get_object_or_404(Projects, id=project_id)
        issue = get_object_or_404(Issues, id=issue_id)

        data = request.data.copy()
        data['project'] = project.id
        data['author'] = issue.author.id

        try:
            Contributors.objects.get(id=data['assignee'], project=project.id)
            serializer = IssuesSerializer(issue, data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Contributors.DoesNotExist:
            return Response(
                "Cet utilisateur n'existe pas.",
                status=status.HTTP_400_BAD_REQUEST
            )

    def delete(self, request, project_id, issue_id):
        issue = get_object_or_404(Issues, id=issue_id)
        issue.delete()
        return Response("Problème supprimé avec succès.", status=status.HTTP_204_NO_CONTENT)
    

class CommentListView(APIView):
    permission_classes = [IsAuthenticated, CommentsPermissions]

    def get(self, request, project_id, issue_id):
        get_object_or_404(Projects, id=project_id)
        issue = get_object_or_404(Issues, id=issue_id)

        comments = Comments.objects.filter(issue=issue)
        serializer = CommentsSerializer(comments, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, project_id, issue_id):
        get_object_or_404(Projects, id=project_id)
        issue = get_object_or_404(Issues, id=issue_id)

        data = request.data.copy()
        data['issue'] = issue.id
        data['author'] = request.user.id
        #print(data)

        serializer = CommentsSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated, CommentsPermissions]

    def get(self, request, project_id, issue_id, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        serializer = CommentsSerializer(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, project_id, issue_id, comment_id):
        issue = get_object_or_404(Issues, id=issue_id)
        comment = get_object_or_404(Comments, id=comment_id)

        data = request.data.copy()
        data['issue'] = issue.id
        data['author'] = comment.author.id

        serializer = CommentsSerializer(comment, data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, project_id, issue_id, comment_id):
        comment = get_object_or_404(Comments, id=comment_id)
        comment.delete()
        return Response('Commentaire supprimé avec succès.', status=status.HTTP_204_NO_CONTENT)
