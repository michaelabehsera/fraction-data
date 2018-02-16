from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from apps.dataset.models import DataSet
from .serializers import DataSetCreatSerializer, DataSetDetailSerializer


class DataSetList(viewsets.ModelViewSet):
    """
     This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions for "DataSet" meta info.
    """

    serializer_class = DataSetCreatSerializer

    def get_queryset(self):
        queryset = DataSet.objects.filter(owner=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class DataSetDetail(APIView):
    """
    * Retrieve, Update or Delete a "Data" of a DataSet Instance

    """
    def get_object(self, pk):
        try:
            return DataSet.objects.get(pk=pk)
        except DataSet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = DataSetDetailSerializer(dataset)
        return Response(serializer.data)

    def post(self, request, pk, format=None):
        return self.put(request, pk, format)

    def put(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = DataSetDetailSerializer(dataset, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        dataset = self.get_object(pk)
        serializer = DataSetDetailSerializer(dataset, data=None)
        if serializer.is_valid():
            serializer.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)