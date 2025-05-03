from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CashFlowViewSet,
    CategoryViewSet,
    StatusViewSet,
    SubcategoryViewSet,
    TypeViewSet,
    UserViewSet,
)

router = DefaultRouter()

router.register(r'cashflows', CashFlowViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'statuses', StatusViewSet)
router.register(r'types', TypeViewSet)
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
