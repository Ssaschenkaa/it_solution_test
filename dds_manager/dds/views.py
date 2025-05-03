from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import (
    CashFlowForm,
    CategoryForm,
    StatusForm,
    SubcategoryForm,
    TypeForm,
    UserRegistrationForm,
)
from .models import CashFlow, Category, Status, Subcategory, Type


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form})


@login_required
def cashflow_delete(request, pk):
    flow = get_object_or_404(CashFlow, pk=pk)
    flow.delete()
    return redirect('cashflow_list')


@login_required
def cashflow_list(request):
    cashflows = CashFlow.objects.filter(
        author=request.user).order_by('-pub_date')

    # Фильтрация
    filters = Q()
    if request.GET.get('pub_date__gte'):
        filters &= Q(pub_date__date__gte=request.GET['pub_date__gte'])
    if request.GET.get('pub_date__lte'):
        filters &= Q(pub_date__date__lte=request.GET['pub_date__lte'])
    if request.GET.get('status__slug'):
        filters &= Q(status__slug=request.GET['status__slug'])
    if request.GET.get('type__slug'):
        filters &= Q(type__slug=request.GET['type__slug'])
    if request.GET.get('category__slug'):
        filters &= Q(category__slug=request.GET['category__slug'])
    if request.GET.get('subcategory__slug'):
        filters &= Q(subcategory__slug=request.GET['subcategory__slug'])

    cashflows = cashflows.filter(filters)

    context = {
        'cashflows': cashflows,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
    }
    return render(request, 'cashflow_list.html', context)


@login_required
def cashflow_form(request, pk=None):
    instance = CashFlow.objects.get(pk=pk) if pk else None
    if request.method == 'POST':
        form = CashFlowForm(request.POST, instance=instance)
        if form.is_valid():
            flow = form.save(commit=False)
            flow.author = request.user
            flow.save()
            return redirect('cashflow_list')
    else:
        form = CashFlowForm(instance=instance)
    return render(request, 'cashflow_form.html', {'form': form})


@login_required
def reference_manage(request):
    tab = request.GET.get('tab', 'status')
    forms_dict = {
        'status': (Status, StatusForm),
        'type': (Type, TypeForm),
        'category': (Category, CategoryForm),
        'subcategory': (Subcategory, SubcategoryForm),
    }
    model, form_class = forms_dict[tab]

    # Редактирование
    if 'edit' in request.GET:
        obj = model.objects.get(pk=request.GET['edit'])
        form = form_class(instance=obj)
    elif request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect(f'?tab={tab}')
    else:
        form = form_class()

    if 'delete' in request.GET:
        model.objects.filter(pk=request.GET['delete']).delete()
        return redirect(f'?tab={tab}')

    context = {
        'tab': tab,
        'form': form,
        'object_list': model.objects.all(),
    }
    return render(request, 'reference_manage.html', context)
