from django import forms

from users.models import User

from .models import CashFlow, Category, Status, Subcategory, Type


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        exclude = ('author', 'pub_date')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['subcategory'].queryset = Subcategory.objects.all()
        self.fields['category'].queryset = Category.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        cash_type = cleaned_data.get('type')
        category = cleaned_data.get('category')
        subcategory = cleaned_data.get('subcategory')

        if cash_type and category:
            if category.type != cash_type:
                valid_categories = Category.objects.filter(type=cash_type)
                valid_names = ", ".join(cat.name for cat in valid_categories)
                self.add_error(
                    'category',
                    f'Выбранная категория не принадлежит типу "{cash_type}". '
                    f'Подходящие категории: {valid_names or "отсутствуют"}.'
                )

        if category and subcategory:
            if subcategory.category != category:
                valid_subs = Subcategory.objects.filter(category=category)
                valid_names = ", ".join(sub.name for sub in valid_subs)
                self.add_error(
                    'subcategory',
                    f'Подкатегория "{subcategory}" не принадлежит категории "{category}". '
                    f'Подходящие подкатегории: {valid_names or "отсутствуют"}.'
                )

        return cleaned_data


class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name', 'slug']


class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name', 'slug']


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'slug', 'type']


class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'slug', 'category']
