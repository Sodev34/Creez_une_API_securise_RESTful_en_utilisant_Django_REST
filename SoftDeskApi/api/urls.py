from django.urls import path

from api import views

urlpatterns = [
    path('projects/', views.ProjectList.as_view()),
    path('projects/<int:project_id>/', views.ProjectDetail.as_view()),
    path('projects/<int:project_id>/users/', views.ContributorList.as_view()),
    path('projects/<int:project_id>/users/<int:user_id>/', views.DeleteContributor.as_view()),

    path('projects/<int:project_id>/issues/', views.IssueList.as_view()),
 
]