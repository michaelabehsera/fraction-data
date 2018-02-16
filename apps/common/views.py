from django.views.generic.base import TemplateView
from rest_framework.authtoken.models import Token

from .mixins import LoginRequiredMixin
from apps.dataset.models import DataSet


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['dataset_list'] = DataSet.objects.all()

        context['api_token'] = Token.objects.get(user=self.request.user)

        context['host_url'] = "http://" + self.request.get_host()

        return context
