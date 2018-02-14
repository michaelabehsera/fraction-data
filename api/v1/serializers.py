from rest_framework import serializers

from apps.dataset.models import DataSet


class DataSetCreatSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('name', 'description', 'column_names')


class DataSetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSet
        fields = ('data',)

