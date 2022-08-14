from django.db.models import IntegerChoices


class UserRole(IntegerChoices):
    DEVELOPER = 0, 'Developer',
    PROJECT_MANAGER = 1, 'Project Manager'
