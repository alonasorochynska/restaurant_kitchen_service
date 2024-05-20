from django.test import TestCase
from kitchen.models import Worker, Position, Dish, Order
from kitchen.forms import (
    WorkerCreationForm, WorkerUpdateForm, WorkerSearchForm,
    PositionCreateForm, PositionUpdateForm, PositionSearchForm,
    DishCreateForm, DishUpdateForm, DishSearchForm,
    OrderCreateForm, OrderUpdateForm, OrderSearchForm
)


class FormsTest(TestCase):

    def setUp(self):
        self.position = Position.objects.create(name="Chef", lead_position=True)
        self.worker = Worker.objects.create_user(username="testuser",
                                                 password="password",
                                                 position=self.position)
        self.dish = Dish.objects.create(name="Pasta", price=10.0)
        self.order = Order.objects.create(worker=self.worker, deadline=60)
        self.order.dishes.add(self.dish)

    def test_worker_creation_form(self):
        form_data = {
            "username": "newuser",
            "password1": "password123!",
            "password2": "password123!",
            "first_name": "New",
            "last_name": "User",
            "position": self.position.id
        }
        form = WorkerCreationForm(data=form_data)
        self.assertTrue(form.is_valid(), form.errors)
        worker = form.save()
        self.assertEqual(worker.username, "newuser")

    def test_worker_update_form(self):
        form_data = {
            "first_name": "Updated",
            "last_name": "User",
            "position": self.position.id
        }
        form = WorkerUpdateForm(data=form_data, instance=self.worker)
        self.assertTrue(form.is_valid())
        worker = form.save()
        self.assertEqual(worker.first_name, "Updated")

    def test_worker_search_form(self):
        form_data = {"username": "testuser"}
        form = WorkerSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "testuser")

    def test_position_create_form(self):
        form_data = {"name": "Manager", "lead_position": True}
        form = PositionCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        position = form.save()
        self.assertEqual(position.name, "Manager")

    def test_position_update_form(self):
        form_data = {"lead_position": False}
        form = PositionUpdateForm(data=form_data, instance=self.position)
        self.assertTrue(form.is_valid())
        position = form.save()
        self.assertFalse(position.lead_position)

    def test_position_search_form(self):
        form_data = {"name": "Chef"}
        form = PositionSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Chef")

    def test_dish_create_form(self):
        form_data = {"name": "Pizza", "note": "Tasty", "price": 15.0}
        form = DishCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        dish = form.save()
        self.assertEqual(dish.name, "Pizza")

    def test_dish_update_form(self):
        form_data = {"price": 12.0}
        form = DishUpdateForm(data=form_data, instance=self.dish)
        self.assertTrue(form.is_valid())
        dish = form.save()
        self.assertEqual(dish.price, 12.0)

    def test_dish_search_form(self):
        form_data = {"name": "Pasta"}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Pasta")

    def test_order_create_form(self):
        form_data = {
            "note": "New order",
            "worker": self.worker.id,
            "deadline": 30,
            "dishes": [self.dish.id]
        }
        form = OrderCreateForm(data=form_data)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertEqual(order.note, "New order")

    def test_order_update_form(self):
        form_data = {
            "note": "Updated order",
            "worker": self.worker.id,
            "deadline": 45,
            "dishes": [self.dish.id]
        }
        form = OrderUpdateForm(data=form_data, instance=self.order)
        self.assertTrue(form.is_valid())
        order = form.save()
        self.assertEqual(order.note, "Updated order")

    def test_order_search_form(self):
        form_data = {
            "worker": self.worker.id,
            "creation_date": "2024-01-01"
        }
        form = OrderSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["worker"], self.worker)
