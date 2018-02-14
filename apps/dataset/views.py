from django.views.generic.base import TemplateView

from apps.common.mixins import LoginRequiredMixin
from .models import DataSet


class DataSetCreateView(LoginRequiredMixin, TemplateView):

    template_name = 'dataset/create_dataset.html'


class DataSetDetailView(LoginRequiredMixin, TemplateView):
    template_name = 'dataset/detail_dataset.html'

    def get_context_data(self, **kwargs):
        context = super(DataSetDetailView, self).get_context_data(**kwargs)

        dataset_id = self.kwargs['dataset_id']

        context['dataset_list'] = DataSet.objects.all()
        try:
            dataset_obj = DataSet.objects.get(id=dataset_id)

        except DataSet.DoesNotExist:
            dataset_obj = None

        context['dataset_obj'] = dataset_obj
        context['api_url'] = "/api/v1/dataset/%s/data/" % dataset_id
        context['host_url'] = self.request.get_host()

        return context

