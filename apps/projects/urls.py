from django.urls import include, path
from rest_framework import routers
from apps.projects.views import ProjectViewSet, TaskViewSet

router = routers.DefaultRouter()
router.register('projects', ProjectViewSet, basename='projects')
router.register('tasks', TaskViewSet, basename='tasks')

urlpatterns = [
    path(r'', include(router.urls)),
]
