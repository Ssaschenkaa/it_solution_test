from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import include, path

from dds.views import (
    cashflow_delete,
    cashflow_form,
    cashflow_list,
    reference_manage,
    register,
)

urlpatterns = [
    path('', cashflow_list, name='cashflow_list'),
    path('add/', cashflow_form, name='cashflow_add'),
    path('edit/<int:pk>/', cashflow_form, name='cashflow_edit'),
    path('delete/<int:pk>/', cashflow_delete, name='cashflow_delete'),  # <- добавлено
    path('references/', reference_manage, name='reference_manage'),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='cashflow_list'), name='logout'),
    path('register/', register, name='register'),
]
