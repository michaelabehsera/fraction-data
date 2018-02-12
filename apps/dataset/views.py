from django.views.generic.edit import CreateView

from apps.common.mixins import LoginRequiredMixin
from .forms import OrderCreateForm


class OrderCreateView(LoginRequiredMixin, CreateView):

    template_name = 'dataset/create_order.html'
    form_class = OrderCreateForm
    success_url = '/'
