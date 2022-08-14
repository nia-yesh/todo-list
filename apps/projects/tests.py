from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from apps.accounts.models import User
from apps.projects.models import Project, Task
from utils.enums import UserRole


class ProjectTest(APITestCase):
    fixtures = [
        'users.json',
        'projects.json',
        'tasks.json'
    ]

    def setUp(self) -> None:
        self.projects_url = reverse('projects-list')

    def authenticate_client(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        return self.client

    def test_all_project_all_tasks(self):
        # test getting all projects and all of their tasks using both users' roles
        for user in User.objects.filter(id__in=(2, 3)):
            response = self.authenticate_client(user).get(self.projects_url, )
            projects = response.json()
            self.assertEqual(len(projects), Project.objects.all().count())
            for project in projects:
                self.assertCountEqual(list(Project.objects.get(id=project['id']).tasks.values_list('id', flat=True)),
                                      [itm['id'] for itm in project['tasks']])

    def test_project_all_tasks(self):
        # test getting a specific project and all of its tasks using both users' roles
        for user in User.objects.filter(id__in=(2, 3)):
            project = Project.objects.last()
            response = self.authenticate_client(user).get(f"{self.projects_url}{project.id}/", )
            result = response.json()
            self.assertCountEqual(list(project.tasks.values_list('id', flat=True)),
                                  [itm['id'] for itm in result['tasks']])


class TaskTest(APITestCase):
    fixtures = [
        'users.json',
        'projects.json',
        'tasks.json'
    ]

    def setUp(self) -> None:
        self.tasks_url = reverse('tasks-list')

    def authenticate_client(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + str(refresh.access_token))
        return self.client

    def test_all_tasks(self):
        # test getting all the tasks of all the projects using both users' roles
        for user in User.objects.filter(id__in=(2, 3)):
            response = self.authenticate_client(user).get(self.tasks_url, )
            result = response.json()
            # check if result count is equal to all tasks count
            self.assertEqual(len(result), Task.objects.all().count())

    def test_tasks_of_project(self):
        # test getting all tasks of a specific project using both users' roles
        for user in User.objects.filter(id__in=(2, 3)):
            project = Project.objects.first()
            response = self.authenticate_client(user).get(f"{self.tasks_url}?project={project.id}", )
            result = response.json()
            # check if all project's tasks are returned
            self.assertCountEqual(list(project.tasks.values_list('id', flat=True)),
                                  [itm['id'] for itm in result])

    def test_tasks_of_user(self):
        # test getting all tasks of a specific user using both users' roles
        for user in User.objects.filter(id__in=(2, 3)):
            response = self.authenticate_client(user).get(f"{self.tasks_url}?assignees={user.id}", )
            result = response.json()
            # check if all user's tasks are returned
            self.assertCountEqual(Task.objects.filter(assignees=user).values_list('id', flat=True),
                                  [itm['id'] for itm in result])

    def test_update_dev_user_task(self):
        user = User.objects.filter(role=UserRole.DEVELOPER, ).first()
        client = self.authenticate_client(user)
        NEW_TITLE = 'changed title'

        # TEST UPDATE A TASK THAT IS ASSIGNED TO USER
        task = Task.objects.filter(assignees=user).first()
        response = client.patch(f"{self.tasks_url}{task.id}/", data={'title': NEW_TITLE})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        task.refresh_from_db()
        self.assertEqual(task.title, NEW_TITLE)

        # TEST UPDATE A TASK THAT IS NOT ASSIGNED TO USER
        task = Task.objects.exclude(assignees=user).first()
        response = client.patch(f"{self.tasks_url}{task.id}/", data={'title': NEW_TITLE})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')
        task.refresh_from_db()
        self.assertNotEqual(task.title, NEW_TITLE)

    def test_update_manager_user_task(self):
        user = User.objects.filter(role=UserRole.PROJECT_MANAGER, ).first()
        client = self.authenticate_client(user)
        NEW_TITLE = 'changed title by manager'

        # TEST UPDATING TASKS THAT ARE ASSIGNED OR NOT ASSIGNED TO MANAGER
        tasks = Task.objects.filter(id__in=[1, 3])
        for task in tasks:
            response = client.patch(f"{self.tasks_url}{task.id}/", data={'title': NEW_TITLE})
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            task.refresh_from_db()
            self.assertEqual(task.title, NEW_TITLE)

    def test_delete_dev_user_task(self):
        user = User.objects.filter(role=UserRole.DEVELOPER, ).first()
        client = self.authenticate_client(user)

        # TEST DELETE A TASK THAT IS ASSIGNED TO USER
        task = Task.objects.filter(assignees=user).first()
        response = client.delete(f"{self.tasks_url}{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        # TEST DELETE A TASK THAT IS NOT ASSIGNED TO USER
        task = Task.objects.exclude(assignees=user).first()
        response = client.delete(f"{self.tasks_url}{task.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json()['detail'], 'You do not have permission to perform this action.')

    def test_delete_manager_user_task(self):
        user = User.objects.filter(role=UserRole.PROJECT_MANAGER, ).first()
        client = self.authenticate_client(user)

        # TEST DELETING TASKS THAT ARE ASSIGNED OR NOT ASSIGNED TO MANAGER
        tasks = Task.objects.filter(id__in=[1, 3])
        for task in tasks:
            response = client.delete(f"{self.tasks_url}{task.id}/")
            self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
