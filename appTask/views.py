from django.shortcuts import render

from .serializers import (
    TaskSerializer,
    TaskUpdateSerializer,
    CommentSerializer,
    CommentCreateSerializer,
    CommentUpdateSerializer,
)
from .models import Task, Comment
from appAuth.models import User
from appProject.models import Project
from django.shortcuts import render


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)

from rest_framework import status
from rest_framework.response import Response

from drf_spectacular.utils import extend_schema


class TaskListView(generics.ListAPIView):  # This api will response a list of all task
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    queryset = Task.objects.all()


class TaskCreateView(generics.CreateAPIView):
    serializer_class = TaskSerializer
    permission_class = [AllowAny]
    queryset = Task.objects.all()

    @extend_schema(
        description="This is for task create API. Give valid user and project id to the assigned_to and project respectively.",
    )
    def create(self, request, *args, **kwargs):
        title = request.data["title"]
        description = request.data["description"]
        status = request.data["status"]
        priority = request.data["priority"]
        assigned_to = request.data["assigned_to"]
        project = request.data["project"]
        due_date = request.data["due_date"]

        user = User.objects.filter(id=assigned_to).first()

        if user is None:
            return Response({"message": "User not found."})

        project_filter = Project.objects.filter(id=project).first()

        if project_filter is None:
            return Response({"message": "Project not found."})

        print(project_filter)
        print(user)

        task = Task()

        task.title = title
        task.description = description
        task.status = status
        task.priority = priority
        task.project = project_filter
        task.assigned_to = user
        task.due_date = due_date
        task.save()

        return Response(({"message": "Task created successfully."}))


class TaskDetailsView(generics.RetrieveAPIView):
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    queryset = Task.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is for task details API. Give a valid  id(task id).",
    )
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        task = Task.objects.get(id=id)
        assigned_to = task.assigned_to
        project = task.project

        data = {
            "id": project.id,
            "title": task.title,
            "description": task.description,
            "status": task.status,
            "priority": task.priority,
            "created_at": project.created_at,
            "assigned_to": {
                "id": assigned_to.id,
                "username": assigned_to.username,
                "email": assigned_to.email,
            },
            "project": {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "owner": {
                    "id": project.owner.id,
                    "username": project.owner.username,
                    "email": project.owner.email,
                },
                "created-at": project.created_at,
            },
        }
        return Response(data, status=status.HTTP_200_OK)


class TaskUpdateView(generics.UpdateAPIView):
    serializer_class = TaskUpdateSerializer
    permission_classes = [AllowAny]
    queryset = Task.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is for task update API. Give a valid id(task id).",
    )
    def perform_update(self, serializer):
        serializer.save()
        return serializer.data


class TaskDeleteView(generics.DestroyAPIView):
    serializer_class = TaskSerializer
    permission_classes = [AllowAny]
    queryset = Task.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is for task delete API. Give a valid id(task id).",
    )
    def destroy(self, request, *args, **kwargs):

        task = self.get_object()
        task.delete()

        return Response(
            {"message": "Task deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )


# Comment views start form here
class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]

    @extend_schema(
        description="This api will response a list of comment of specific task. Give a valid id(task id).",
    )
    def get_queryset(self):
        task = self.kwargs.get("task")
        comments = Comment.objects.filter(task=task)
        return comments


class CommentCreateView(generics.CreateAPIView):
    serializer_class = CommentCreateSerializer
    permission_class = [AllowAny]
    queryset = Comment.objects.all()

    @extend_schema(
        description="This is comment create API. Give valid task_id and user_id.",
    )
    def create(self, request, *args, **kwargs):

        task_id = kwargs.get("task_id")
        user_id = request.data["user"]
        content = request.data["content"]
        task = Task.objects.filter(id=task_id).first()
        user = User.objects.filter(id=user_id).first()

        if task is None:
            return Response(
                {"message": "Task not found"}, status=status.HTTP_404_NOT_FOUND
            )

        if user is None:
            return Response(
                {"message": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )

        comment = Comment()
        comment.content = content
        comment.user = user
        comment.task = task
        comment.save()

        return Response(({"message": "Comment created successfully."}))


class CommentDetailsView(generics.RetrieveAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is comment details API. Give a valid id(comment id)",
    )
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        comment = Comment.objects.get(id=id)
        user = comment.user
        task = comment.task

        data = {
            "id": comment.id,
            "content": comment.content,
            "created_at": comment.create_at,
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "task": {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "status": task.status,
                "priority": task.priority,
            },
        }

        return Response(data, status=status.HTTP_200_OK)


class CommentUpdateView(generics.UpdateAPIView):
    serializer_class = CommentUpdateSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is comment update API. Give a valid id(comment if).",
    )
    def perform_update(self, serializer):
        serializer.save()
        return serializer.data


class CommentDeleteView(generics.DestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]
    queryset = Comment.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is comment delete API. Give a valid id(comment id).",
    )

    def destroy(self, request, *args, **kwargs):

        comment = self.get_object()
        comment.delete()

        return Response(
            {"message": "Comment deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
