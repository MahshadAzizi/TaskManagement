from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend

from tasks.queries import get_tasks_all
from customize.views import CustomViewSet
from tasks.serializers import TaskSerializer, CreateTaskSerializer
from tasks.filters import TaskFilter
from users.permissions import IsOwner


class TaskView(CustomViewSet):
    queryset = get_tasks_all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter
    allowed_methods = ['get', 'post']

    def get_serializer_class(self):
        if self.action == 'list':
            return TaskSerializer
        else:
            return CreateTaskSerializer


class TaskDetailView(CustomViewSet):
    queryset = get_tasks_all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]
    allowed_methods = ['get', 'patch', 'delete']

    def get_permissions(self):
        if self.action == 'destroy':
            return [IsOwner()]
        else:
            return [IsAuthenticated()]
