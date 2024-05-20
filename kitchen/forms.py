from django import forms
from django.contrib.auth.forms import UserCreationForm

from kitchen.models import Worker, Order, Position, Dish


class WorkerCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Worker
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "position")


class WorkerUpdateForm(forms.ModelForm):
    class Meta:
        model = Worker
        fields = ("first_name", "last_name", "position")


class WorkerSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by username"}
        ),
    )


class PositionCreateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = "__all__"


class PositionUpdateForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ("lead_position", "kitchen")


class PositionSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        ),
    )


class DishCreateForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = "__all__"


class DishUpdateForm(forms.ModelForm):
    class Meta:
        model = Dish
        fields = ("price",)


class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Search by name"}
        ),
    )


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("dishes", "note", "worker", "deadline")


class OrderUpdateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ("dishes", "note", "worker", "deadline")


class OrderSearchForm(forms.Form):
    worker = forms.ModelChoiceField(
        queryset=Worker.objects.all(),
        required=False,
        label="Worker",
        widget=forms.Select(attrs={"class": "form-control"})
    )
    creation_date = forms.DateField(
        required=False,
        label="Creation Date",
        widget=forms.DateInput(
            attrs={"type": "date", "class": "form-control"}
        )
    )
