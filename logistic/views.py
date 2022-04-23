from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination

from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['title', 'description']


class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    pagination_class = LimitOffsetPagination

    def get_queryset(self):

        id = self.request.query_params.get('products')

        if id is not None:
            queryset = self.queryset.filter(products__id=id)
        return queryset
