from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Project, Task, Label, Comment

User = get_user_model()


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ["id", "name", "description", "created_at"]
        read_only_fields = ["id", "created_at"]


class LabelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Label
        fields = ["id", "name", "created_at"]
        read_only_fields = ["id", "created_at"]


class TaskSerializer(serializers.ModelSerializer):
    labels = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Label.objects.all(), required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        request = self.context.get("request")
        if not request or not request.user or not request.user.is_authenticated:
            return

        user = request.user
        is_admin = user.is_staff or user.is_superuser

        if "project" in self.fields:
            if is_admin:
                self.fields["project"].queryset = Project.objects.all()
            else:
                self.fields["project"].queryset = Project.objects.filter(owner=user)

        if "labels" in self.fields:
            if is_admin:
                self.fields["labels"].queryset = Label.objects.all()
            else:
                self.fields["labels"].queryset = Label.objects.filter(owner=user)


    class Meta:
        model = Task
        fields = [
            "id",
            "project",
            "title",
            "description",
            "status",
            "priority",
            "due_date",
            "labels",
            "created_at",
            "completed_at",
        ]
        read_only_fields = ["id", "created_at", "completed_at"]

    def validate_project(self, project):
        """
        Projekt musi należeć do zalogowanego użytkownika.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated and project.owner_id != request.user.id:
            raise serializers.ValidationError("You can only use your own projects.")
        return project

    def validate_labels(self, labels):
        """
        Etykiety muszą należeć do zalogowanego użytkownika.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated:
            for label in labels:
                if label.owner_id != request.user.id:
                    raise serializers.ValidationError("You can only use your own labels.")
        return labels


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id", "task", "content", "created_at"]
        read_only_fields = ["id", "created_at"]

    def validate_task(self, task):
        """
        Nie pozwalamy komentować cudzych zadań.
        """
        request = self.context.get("request")
        if request and request.user.is_authenticated and task.owner_id != request.user.id:
            raise serializers.ValidationError("You can only comment on your own tasks.")
        return task
