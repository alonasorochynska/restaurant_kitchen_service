from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from .models import Worker, Order, Dish, Position


@admin.register(Worker)
class WorkerAdmin(UserAdmin):
    list_display = ("username", "id", "position", "get_order_count")
    fieldsets = UserAdmin.fieldsets + (
        (("Additional info", {"fields": ("position",)}),)
    )
    add_fieldsets = UserAdmin.add_fieldsets + (((
        "Additional info",
        {"fields": ("first_name", "last_name", "position",)},
        ),))

    def get_order_count(self, obj):
        return obj.orders.count()

    get_order_count.short_description = "Number of Orders"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = admin.ModelAdmin.list_display + ("worker", "is_completed", "creation_time", "completion_time")
    search_fields = ("name",)
    list_filter = ("dishes",)


@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price")


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "lead_position")


admin.site.unregister(Group)
