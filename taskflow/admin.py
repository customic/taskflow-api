from django.contrib import admin

from .models import Comment, Label, Project, Task

admin.site.register(Project)
admin.site.register(Task)
admin.site.register(Label)
admin.site.register(Comment)
