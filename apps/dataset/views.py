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

        context['dataset_name'] = dataset_obj.name
        context['dataset_desc'] = dataset_obj.description

        column_names = dataset_obj.column_names

        context['col_names'] = column_names.keys() if column_names is not None else None
        context['col_descs'] = column_names.values() if column_names is not None else None
        context['columns'] = zip(context['col_names'], context['col_descs']) if column_names is not None else None

        context['api_url'] = "/api/v1/dataset/%s/data/" % dataset_id
        context['host_url'] = self.request.get_host()

        return context

