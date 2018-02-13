from django.views.generic.base import View
from django.shortcuts import redirect

from .mixins import LoginRequiredMixin
from apps.dataset.models import Order


class HomeView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        first_order = Order.objects.first()
        if first_order is None:
            return redirect('/dataset/create_order/')
        else:
            return redirect('/dataset/order_detail/%d/' % first_order.id)
