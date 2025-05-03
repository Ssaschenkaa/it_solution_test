import re

from rest_framework import serializers

from dds.models import CashFlow, Category, Status, Subcategory, Type
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'type')


class SubcategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Subcategory
        fields = ('id', 'name', 'slug', 'category')


class StatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = Status
        fields = ('id', 'name', 'slug')


class TypeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Type
        fields = ('id', 'name', 'slug')


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            'email', 'id', 'username', 'first_name',
            'last_name', 'password',
        ]

    def validate_username(self, value):
        if not re.fullmatch(r'^[\w.@+-]+\Z', value):
            raise serializers.ValidationError(
                'Имя должно соответствовать паттерну ^[\\w.@+-]+\\Z')
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class CashFlowSerializer(serializers.ModelSerializer):
    pub_date = serializers.SerializerMethodField()
    category = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Category.objects.all(), required=True
    )
    subcategory = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Subcategory.objects.all(), required=True
    )
    status = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Status.objects.all()
    )
    type = serializers.SlugRelatedField(
        slug_field='slug',
        queryset=Type.objects.all(), required=True
    )
    amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, required=True)

    class Meta:
        model = CashFlow
        fields = [
            'pub_date', 'status', 'type', 'category',
            'subcategory', 'amount', 'comment'
        ]

    def validate(self, data):
        category = data.get('category')
        subcategory = data.get('subcategory')
        type_ = data.get('type')

        if category.type != type_:
            raise serializers.ValidationError(
                f"Категория '{category.name}' не соответствует выбранному типу '{type_.name}'."
            )

        if subcategory.category != category:
            raise serializers.ValidationError(
                f"Подкатегория '{subcategory.name}' не принадлежит категории '{category.name}'."
            )

        return data

    def get_pub_date(self, obj):
        return obj.pub_date.strftime('%d.%m.%Y')
