from django.urls import path
from . import views


urlpatterns = [
    #   Task urls start from here
    path("create/", views.TaskCreateView.as_view()),
    path("list/", views.TaskListView.as_view()),
    path("details/<int:id>/", views.TaskDetailsView.as_view()),
    path("update/<int:id>/", views.TaskUpdateView.as_view()),
    path("delete/<int:id>/", views.TaskDeleteView.as_view()),
    #  Comment urls start from here
    path("comments/create/<int:task_id>/", views.CommentCreateView.as_view()),
    path("comments/list/<int:id>/", views.CommentListView.as_view()),
    path("comments/details/<int:id>/", views.CommentDetailsView.as_view()),
    path("comments/update/<int:id>/", views.CommentUpdateView.as_view()),
    path("comments/delete/<int:id>/", views.CommentDeleteView.as_view()),
]
