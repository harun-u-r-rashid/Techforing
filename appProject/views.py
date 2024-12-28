from django.shortcuts import render


from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import (
    AllowAny,
    IsAuthenticated,
)


from rest_framework import status
from rest_framework.response import Response

from .serializers import ProjectSerializer, ProjectUpdateSerializer
from .models import Project
from appAuth.models import User

from drf_spectacular.utils import extend_schema


class ProjectListView(
    generics.ListAPIView
):  # This API will response a list of all projects.
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()


class ProjectCreateView(generics.CreateAPIView):
    serializer_class = ProjectSerializer
    permission_class = [AllowAny]
    queryset = Project.objects.all()

    @extend_schema(
        description="This is for project creation API. Give a valid user id into the owner field.",
    )
    def create(self, request, *args, **kwargs):
        owner = request.data["owner"]
        name = request.data["name"]
        description = request.data["description"]
        user = User.objects.filter(id=owner).first()
        project = Project()
        project.owner = user
        project.name = name
        project.description = description
        project.save()

        return Response(({"message": "Project created successfully."}))


class ProjectDetailsView(generics.RetrieveAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is for project details API. Give a valid id(project id).",
    )
    def retrieve(self, request, *args, **kwargs):
        id = self.kwargs["id"]
        project = Project.objects.get(id=id)
        owner = project.owner

        data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "owner": {"id": owner.id, "username": owner.username, "email": owner.email},
        }
        return Response(data, status=status.HTTP_200_OK)


class ProjectUpdateView(generics.UpdateAPIView):
    serializer_class = ProjectUpdateSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    lookup_field = "id"
    @extend_schema(
        description="This is for project update API. Give a valid id (project id).",

    )

    def perform_update(self, serializer):
        serializer.save()
        return serializer.data


class ProjectDeleteView(generics.DestroyAPIView):
    serializer_class = ProjectSerializer
    permission_classes = [AllowAny]
    queryset = Project.objects.all()
    lookup_field = "id"

    @extend_schema(
        description="This is for project delete API. Give a valid id (project id).",

    )

    def destroy(self, request, *args, **kwargs):
        project = self.get_object()
        project.delete()

        return Response(
            {"message": "Project deleted successfully."},
            status=status.HTTP_204_NO_CONTENT,
        )
