from django.contrib import admin
from django import forms
from .models import Category, Subcategory, Type, Status, CashFlow

class CashFlowAdminForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Ограничиваем категории по выбранному типу
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)

        # Ограничиваем подкатегории по выбранной категории
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)

class CashFlowAdmin(admin.ModelAdmin):
    form = CashFlowAdminForm

admin.site.register(Category)
admin.site.register(Subcategory)
admin.site.register(Type)
admin.site.register(Status)
admin.site.register(CashFlow, CashFlowAdmin)