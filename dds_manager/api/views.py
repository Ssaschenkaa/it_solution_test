from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from dds.models import CashFlow, Category, Status, Subcategory, Type
from users.models import User

from .serializers import (
    CashFlowSerializer,
    CategorySerializer,
    StatusSerializer,
    SubcategorySerializer,
    TypeSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer


class CashFlowViewSet(viewsets.ModelViewSet):
    queryset = CashFlow.objects.all().order_by('pub_date')
    serializer_class = CashFlowSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]

    filterset_fields = {
        'pub_date': ['gte', 'lte'],
        'status__slug': ['exact'],
        'subcategory__slug': ['exact'],
        'category__slug': ['exact'],
        'type__slug': ['exact'],
    }

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all().order_by('name')
    serializer_class = TypeSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all().order_by('name')
    serializer_class = StatusSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('name')
    serializer_class = CategorySerializer


class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all().order_by('name')
    serializer_class = SubcategorySerializer
