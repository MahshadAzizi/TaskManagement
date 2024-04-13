from rest_framework.permissions import BasePermission

from tasks.queries import get_task_by_id


class IsAdminRule(BasePermission):
    def has_permission(self, request, view):
        if request.user and request.user.user_type == 'admin':
            return True
        else:
            return False


class IsOwner(BasePermission):
    def has_permission(self, request, view):
        task = get_task_by_id(pk=view.kwargs.get('pk'))
        if task.assigner == request.user:
            return True
        else:
            return False
