from django.urls import path

from api import views

urlpatterns = [
    path('projects/', views.ProjectListView.as_view()),
    path('projects/<int:project_id>/', views.ProjectDetailView.as_view()),
    path('projects/<int:project_id>/users/', views.ContributorListView.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>/', views.DeleteContributorView.as_view()),

    path('projects/<int:project_id>/issues/', views.IssueListView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/', views.IssueDetailView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/', views.CommentListView.as_view()),
    path('projects/<int:project_id>/issues/<int:issue_id>/comments/<int:comment_id>/', views.CommentDetailView.as_view()),
]
 
