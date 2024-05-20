from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.admin.sites import AdminSite
from kitchen.models import Worker, Order, Dish, Position
from kitchen.admin import WorkerAdmin, OrderAdmin, DishAdmin, PositionAdmin

User = get_user_model()


class MockRequest:
    pass


class AdminTests(TestCase):

    def setUp(self):
        self.site = AdminSite()
        self.position = Position.objects.create(name="Chef", lead_position=True)
        self.worker = Worker.objects.create_user(username="testuser", password="password", position=self.position)
        self.dish = Dish.objects.create(name="Pasta", description="Delicious", price=10.0)
        self.order = Order.objects.create(worker=self.worker, note="Test order", deadline=60)
        self.order.dishes.add(self.dish)

    def test_worker_admin(self):
        worker_admin = WorkerAdmin(Worker, self.site)
        request = MockRequest()

        # Test list display
        self.assertEqual(worker_admin.list_display, ("username", "id", "position", "get_order_count"))

        # Test get_order_count method
        self.assertEqual(worker_admin.get_order_count(self.worker), 1)

        # Test fieldsets
        self.assertIn("Additional info", dict(worker_admin.fieldsets))

        # Test add_fieldsets
        self.assertIn("Additional info", dict(worker_admin.add_fieldsets))

    def test_order_admin(self):
        order_admin = OrderAdmin(Order, self.site)
        request = MockRequest()

        # Test list display
        self.assertIn("worker", order_admin.list_display)
        self.assertIn("is_completed", order_admin.list_display)
        self.assertIn("creation_time", order_admin.list_display)
        self.assertIn("completion_time", order_admin.list_display)

        # Test search fields
        self.assertEqual(order_admin.search_fields, ("name",))

        # Test list filter
        self.assertEqual(order_admin.list_filter, ("dishes",))

    def test_dish_admin(self):
        dish_admin = DishAdmin(Dish, self.site)

        # Test list display
        self.assertEqual(dish_admin.list_display, ("name", "price"))

    def test_position_admin(self):
        position_admin = PositionAdmin(Position, self.site)

        # Test list display
        self.assertEqual(position_admin.list_display, ("name", "lead_position"))

    def test_admin_pages(self):
        # Login as superuser
        self.superuser = User.objects.create_superuser(username="admin", password="password", email="admin@example.com")
        self.client.login(username="admin", password="password")

        # Test WorkerAdmin list page
        response = self.client.get(reverse("admin:kitchen_worker_changelist"))
        self.assertEqual(response.status_code, 200)

        # Test OrderAdmin list page
        response = self.client.get(reverse("admin:kitchen_order_changelist"))
        self.assertEqual(response.status_code, 200)

        # Test DishAdmin list page
        response = self.client.get(reverse("admin:kitchen_dish_changelist"))
        self.assertEqual(response.status_code, 200)

        # Test PositionAdmin list page
        response = self.client.get(reverse("admin:kitchen_position_changelist"))
        self.assertEqual(response.status_code, 200)

        # Test WorkerAdmin add page
        response = self.client.get(reverse("admin:kitchen_worker_add"))
        self.assertEqual(response.status_code, 200)

        # Test OrderAdmin add page
        response = self.client.get(reverse("admin:kitchen_order_add"))
        self.assertEqual(response.status_code, 200)

        # Test DishAdmin add page
        response = self.client.get(reverse("admin:kitchen_dish_add"))
        self.assertEqual(response.status_code, 200)

        # Test PositionAdmin add page
        response = self.client.get(reverse("admin:kitchen_position_add"))
        self.assertEqual(response.status_code, 200)
