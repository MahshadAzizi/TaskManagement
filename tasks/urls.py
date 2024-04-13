from django.urls import path
from tasks.views import TaskView, TaskDetailView

urlpatterns = [
    path('', TaskView.as_view({
        'get': 'list',
        'post': 'create'
    }), name='tasks'),
    path('<int:pk>/', TaskDetailView.as_view({
        'get': 'retrieve',
        'patch': 'partial_update',
        'delete': 'destroy'
    }), name='task_detail')
]
