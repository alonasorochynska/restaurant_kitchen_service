from django.test import TestCase
from kitchen.models import Worker, Position


class WorkerModelTests(TestCase):

    def test_worker_creation(self):
        username = "test_worker"
        password = "test1234"
        position = Position.objects.create(name="Chef", lead_position=True)
        worker = Worker.objects.create_user(username=username,
                                            password=password,
                                            position=position)
        self.assertEqual(worker.username, username)
        self.assertTrue(worker.check_password(password))
        self.assertEqual(worker.position, position)
