from django.views.generic.base import TemplateView

from .mixins import LoginRequiredMixin
from apps.dataset.models import DataSet


class HomeView(LoginRequiredMixin, TemplateView):

    template_name = 'home.html'

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)

        context['dataset_list'] = DataSet.objects.all()

        return context
