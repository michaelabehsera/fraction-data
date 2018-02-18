from django.conf.urls import url

from .views import DataSetCreateView, DataSetDetailView


app_name = 'dataset'

urlpatterns = [

    url(r'^create_dataset/$', DataSetCreateView.as_view(), name='create_dataset'),
    url(r'^detail_dataset/(?P<dataset_id>[0-9]+)/$', DataSetDetailView.as_view(), name='detail_dataset'),
]
