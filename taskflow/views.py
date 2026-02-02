from __future__ import annotations

from typing import Any

from django.db.models import QuerySet
from rest_framework import permissions, viewsets
from rest_framework.request import Request

from .models import Comment, Label, Project, Task
from .serializers import CommentSerializer, LabelSerializer, ProjectSerializer, TaskSerializer


class IsAdminOrOwnerOnly(permissions.BasePermission):
    """
    Admin widzi wszystko, zwykły user tylko swoje obiekty.
    """

    def has_object_permission(self, request: Request, view: Any, obj: Any) -> bool:
        if request.user and request.user.is_staff:
            return True

        owner_id = getattr(obj, "owner_id", None)
        if owner_id is not None:
            return owner_id == request.user.id

        author_id = getattr(obj, "author_id", None)
        if author_id is not None:
            return author_id == request.user.id

        return False


class ProjectViewSet(viewsets.ModelViewSet):
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOnly]

    def get_queryset(self) -> QuerySet[Project]:
        qs = Project.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer: ProjectSerializer) -> None:
        serializer.save(owner=self.request.user)


class LabelViewSet(viewsets.ModelViewSet):
    serializer_class = LabelSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOnly]

    def get_queryset(self) -> QuerySet[Label]:
        qs = Label.objects.all()
        if self.request.user.is_staff:
            return qs
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer: LabelSerializer) -> None:
        serializer.save(owner=self.request.user)


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOnly]

    def get_queryset(self) -> QuerySet[Task]:
        qs = Task.objects.select_related("project", "owner").prefetch_related("labels")
        if self.request.user.is_staff:
            return qs
        return qs.filter(owner=self.request.user)

    def perform_create(self, serializer: TaskSerializer) -> None:
        serializer.save(owner=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrOwnerOnly]

    def get_queryset(self) -> QuerySet[Comment]:
        qs = Comment.objects.select_related("task", "author")
        if self.request.user.is_staff:
            return qs
        return qs.filter(author=self.request.user)

    def perform_create(self, serializer: CommentSerializer) -> None:
        serializer.save(author=self.request.user)
