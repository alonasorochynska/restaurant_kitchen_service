from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic

from .forms import (WorkerCreationForm, WorkerUpdateForm,
                    PositionCreateForm, PositionUpdateForm,
                    DishCreateForm, DishUpdateForm,
                    OrderCreateForm, OrderUpdateForm, WorkerSearchForm, PositionSearchForm, OrderSearchForm,
                    DishSearchForm)

from .mixins import LeadPositionRequiredMixin, KitchenPositionRequiredMixin, NotKitchenPositionRequiredMixin

from .models import Worker, Order, Dish, Position


def index(request):
    """View function for the home page of the site."""

    num_workers = Worker.objects.count()
    num_orders = Order.objects.count()
    num_dishes = Dish.objects.count()
    num_positions = Position.objects.count()
    completed_in_time = Order.objects.filter(is_completed_in_time=True).count()

    context = {
        "num_workers": num_workers,
        "num_orders": num_orders,
        "num_dishes": num_dishes,
        "num_positions": num_positions,
        "completed_in_time": completed_in_time
    }

    return render(request, "kitchen/index.html", context=context)


class CompleteOrderView(LoginRequiredMixin,
                        LeadPositionRequiredMixin,
                        NotKitchenPositionRequiredMixin,
                        generic.TemplateView):
    template_name = "kitchen/order_complete.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['order'] = get_object_or_404(Order, pk=self.kwargs['pk'])
        return context

    @staticmethod
    def post(request, pk):
        order = get_object_or_404(Order, pk=pk)
        if request.method == "POST":
            action_type = request.POST.get("action")
            if action_type:
                if action_type == "claim":
                    order.worker = request.user
                    order.save()
                elif action_type == "complete":
                    order.is_completed = True
                    if order.completion_time:
                        order.is_completed_in_time = True
                    order.save()
                return redirect(reverse("kitchen:worker-detail", args=[order.worker.pk]))
        return render(request, "kitchen/order_complete.html", {"order": order})


class WorkerCreateView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.CreateView):
    model = Worker
    form_class = WorkerCreationForm
    success_url = reverse_lazy("kitchen:worker-list")


class WorkerListView(LoginRequiredMixin, generic.ListView):
    model = Worker
    queryset = Worker.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(WorkerListView, self).get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = WorkerSearchForm(
            initial={"username": username}
        )
        return context

    def get_queryset(self):
        form = WorkerSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                username__icontains=form.cleaned_data["username"]
            )
        return self.queryset


class WorkerDetailView(LoginRequiredMixin, generic.DetailView):
    model = Worker
    queryset = Worker.objects.all().prefetch_related("orders__dishes")


class WorkerUpdateView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.UpdateView):
    model = Worker
    form_class = WorkerUpdateForm
    success_url = reverse_lazy("kitchen:worker-list")


class WorkerDeleteView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.DeleteView):
    model = Worker
    success_url = reverse_lazy("kitchen:worker-list")


class PositionCreateView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.CreateView):
    model = Position
    form_class = PositionCreateForm
    success_url = reverse_lazy("kitchen:position-list")


class PositionListView(LoginRequiredMixin, generic.ListView):
    model = Position
    queryset = Position.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(PositionListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = PositionSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = PositionSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class PositionDetailView(LoginRequiredMixin, generic.DetailView):
    model = Position


class PositionUpdateView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.UpdateView):
    model = Position
    form_class = PositionUpdateForm
    success_url = reverse_lazy("kitchen:position-list")


class PositionDeleteView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.DeleteView):
    model = Position
    success_url = reverse_lazy("kitchen:position-list")


class DishCreateView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.CreateView):
    model = Dish
    form_class = DishCreateForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    queryset = Dish.objects.all()
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(DishListView, self).get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(
            initial={"name": name}
        )
        return context

    def get_queryset(self):
        form = DishSearchForm(self.request.GET)
        if form.is_valid():
            return self.queryset.filter(
                name__icontains=form.cleaned_data["name"]
            )
        return self.queryset


class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish


class DishUpdateView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.UpdateView):
    model = Dish
    form_class = DishUpdateForm
    success_url = reverse_lazy("kitchen:dish-list")


class DishDeleteView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.DeleteView):
    model = Dish
    success_url = reverse_lazy("kitchen:dish-list")


class OrderCreateView(LoginRequiredMixin, NotKitchenPositionRequiredMixin, generic.CreateView):
    model = Order
    form_class = OrderCreateForm
    success_url = reverse_lazy("kitchen:order-list")


class OrderListView(LoginRequiredMixin, generic.ListView):
    model = Order
    queryset = Order.objects.all().prefetch_related("dishes")
    paginate_by = 5

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(OrderListView, self).get_context_data(**kwargs)
        dish = self.request.GET.get("dish", "")
        worker = self.request.GET.get("worker", "")
        creation_date = self.request.GET.get("creation_date", "")
        context["search_form"] = OrderSearchForm(
            initial={"dish": dish, "worker": worker, "creation_date": creation_date}
        )
        return context

    def get_queryset(self):
        form = OrderSearchForm(self.request.GET)
        queryset = self.queryset
        if form.is_valid():
            worker = form.cleaned_data["worker"]
            creation_date = form.cleaned_data["creation_date"]
            if worker:
                queryset = queryset.filter(worker=worker)
            if creation_date:
                queryset = queryset.filter(creation_time__date=creation_date)
        return queryset


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    model = Order


class OrderUpdateView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.UpdateView):
    model = Order
    form_class = OrderUpdateForm
    success_url = reverse_lazy("kitchen:order-list")


class OrderDeleteView(LoginRequiredMixin, LeadPositionRequiredMixin, generic.DeleteView):
    model = Order
    success_url = reverse_lazy("kitchen:order-list")
