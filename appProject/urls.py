from django.urls import path
from . import views


urlpatterns = [
    path("create/", views.ProjectCreateView.as_view()),
    path("list/", views.ProjectListView.as_view()),
    path("details/<int:id>/", views.ProjectDetailsView.as_view()),
    path("update/<int:id>/", views.ProjectUpdateView.as_view()),
    path("delete/<int:id>/", views.ProjectDeleteView.as_view()),
]
