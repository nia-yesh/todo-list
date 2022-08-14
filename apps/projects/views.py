from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from apps.projects.models import Project, Task
from apps.projects.permissions import TaskPermission
from apps.projects.serializers import ProjectSerializer, TaskSerializer


class ProjectViewSet(ModelViewSet):
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend]


class TaskViewSet(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = (TaskPermission,)
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['project', 'assignees']
