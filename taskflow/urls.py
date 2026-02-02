from rest_framework.routers import DefaultRouter

from .views import ProjectViewSet, TaskViewSet, LabelViewSet, CommentViewSet

router = DefaultRouter()
router.register(r"projects", ProjectViewSet, basename="project")
router.register(r"tasks", TaskViewSet, basename="task")
router.register(r"labels", LabelViewSet, basename="label")
router.register(r"comments", CommentViewSet, basename="comment")

urlpatterns = router.urls
