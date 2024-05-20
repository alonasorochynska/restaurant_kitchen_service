from django.core.exceptions import PermissionDenied
from django.shortcuts import render
from django.views.generic import View


class LeadPositionRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.position.lead_position:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, "403.html")


class KitchenPositionRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.position.kitchen:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, "403.html")


class NotKitchenPositionRequiredMixin(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.position.kitchen:
            raise PermissionDenied

        return super().dispatch(request, *args, **kwargs)

    def handle_no_permission(self):
        return render(self.request, "403.html")
