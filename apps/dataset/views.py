from django.views.generic.edit import CreateView
from django.views.generic.base import TemplateView

from apps.common.mixins import LoginRequiredMixin
from .forms import OrderCreateForm
from .models import Order


class OrderCreateView(LoginRequiredMixin, CreateView):

    template_name = 'dataset/create_order.html'
    form_class = OrderCreateForm
    success_url = '/'


class OrderDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'dataset/order_detail.html'

    def get_context_data(self, **kwargs):
        context = super(OrderDetailView, self).get_context_data(**kwargs)

        order_id = self.kwargs['order_id']

        context['order_list'] = Order.objects.all()
        try:
            order_obj = Order.objects.get(id=order_id)

        except Order.DoesNotExist:
            order_obj = None

        context['order_obj'] = order_obj
        context['api_url'] = "/api/v1/order/%s/data/" % order_id
        context['host_url'] = self.request.get_host()

        return context

