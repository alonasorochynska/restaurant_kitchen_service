from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.utils import timezone


class Worker(AbstractUser):
    position = models.ForeignKey("Position", on_delete=models.CASCADE,
                                 null=True, blank=True, related_name="workers")

    class Meta:
        verbose_name = "worker"
        verbose_name_plural = "workers"

    def __str__(self):
        return self.username

    def get_absolute_url(self):
        return reverse("kitchen:worker-detail", kwargs={"pk": self.pk})


class Position(models.Model):
    name = models.CharField(max_length=255)
    lead_position = models.BooleanField(default=False)
    kitchen = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kitchen:position-detail", kwargs={"pk": self.pk})


class Dish(models.Model):
    name = models.CharField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("kitchen:dish-detail", kwargs={"pk": self.pk})


class Order(models.Model):
    dishes = models.ManyToManyField(Dish, related_name="orders")
    note = models.TextField(null=True, blank=True)
    worker = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders")
    is_completed = models.BooleanField(default=False)
    is_completed_in_time = models.BooleanField(default=False)
    creation_time = models.DateTimeField(auto_now_add=True)
    deadline = models.IntegerField(default=60)

    def __str__(self):
        return str(self.id)

    @property
    def completion_time(self):
        completion_time = self.creation_time + timezone.timedelta(minutes=self.deadline)
        if completion_time <= timezone.now():
            return False
        return int((completion_time - timezone.now()).total_seconds() // 60)

    def get_dish_names(self):
        return ", ".join(dish.name for dish in self.dishes.all())

    def get_absolute_url(self):
        return reverse("kitchen:order-detail", kwargs={"pk": self.pk})
