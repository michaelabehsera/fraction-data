from django.views.generic.base import TemplateView

from .mixins import LoginRequiredMixin
from apps.dataset.models import Order


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['order_list'] = Order.objects.all()

        return context
