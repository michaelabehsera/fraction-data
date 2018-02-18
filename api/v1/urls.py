from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns

from .views import DataSetList, DataSetDetail


dataset_list = DataSetList.as_view({
    'get': 'list',
    'post': 'create'
})
dataset_meta = DataSetList.as_view({
    'get': 'retrieve',
    'put': 'update',
    'delete': 'destroy'
})

urlpatterns = format_suffix_patterns([
    url(r'^datasets/$', dataset_list, name='dataset-list'),
    url(r'^datasets/(?P<pk>[0-9]+)/$', dataset_meta, name='dataset-meta'),
    url(r'^dataset/(?P<pk>[0-9]+)/data/$', DataSetDetail.as_view()),
])
