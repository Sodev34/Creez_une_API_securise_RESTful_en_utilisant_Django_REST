from rest_framework import serializers

from api.models import Projects, Contributors, Issues, Comments


class ProjectsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Projects
        fields = ("id", "title", "description", "type", "author")
        read_only__fields = ('author', 'id')

class ContributorsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contributors
        fields = ("id", "user", "project", "permission", "role")
        read_only__fields = ('project', 'role', 'id')


class IssuesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Issues
        fields = "__all__"
        read_only__fields = ('project', 'author', 'created_time', 'id')


class CommentsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = "__all__"
        read_only__fields = ('author', 'issue', 'created_time', 'id')