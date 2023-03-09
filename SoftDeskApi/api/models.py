from django.db import models
from django.conf import settings

PERMISSIONS_CHOICES = (
        ("author", "author"),
        ("contributor", "contributor"),
    )

class Projects(models.Model):
    title = models.CharField(max_length=120)
    description = models.CharField(max_length=1200)
    type = models.CharField(max_length=200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name='user', on_delete=models.CASCADE)


class Contributors(models.Model):
    PERMISSIONS_CHOICES = (
        ("author", "author"),
        ("contributor", "contributor"),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Projects, on_delete=models.CASCADE)
    permission= models.CharField(max_length=15, choices=PERMISSIONS_CHOICES, default="contributor")
    role = models.CharField(max_length=15,default="contributor")


class Issues(models.Model):
    title = models.CharField(max_length=120)
    desc = models.CharField(max_length=600)
    tag = models.CharField(max_length=40)
    priority = models.CharField(max_length=40)
    project = models.ForeignKey(Projects, related_name='project', on_delete=models.CASCADE)
    status = models.CharField(max_length=40)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='author',on_delete=models.CASCADE)
    assignee = models.ForeignKey(Contributors, related_name='assignee_user', on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    description = models.TextField(max_length=1200)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issues, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)
