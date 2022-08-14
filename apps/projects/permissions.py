from rest_framework import permissions

from apps.projects.models import Task
from utils.enums import UserRole


class TaskPermission(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj: Task):
        role = request.user.role
        match role:
            # PROJECT_MANAGER can do all actions on all tasks
            case UserRole.PROJECT_MANAGER:
                return True
            # DEVELOPER can do ['update', 'partial_update', 'destroy', ] actions only on his/her tasks
            case UserRole.DEVELOPER:
                if view.action in ['update', 'partial_update', 'destroy', ]:
                    if request.user not in obj.assignees.all():
                        return False
                return True
            case _:
                return False
