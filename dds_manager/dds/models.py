from django.db import models

from users.models import User

NAME_MAX_LENGTH = 64


class CashFlow(models.Model):
    author = models.ForeignKey(
        User, related_name='flows',
        on_delete=models.CASCADE,
        verbose_name='Автор'
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата и время создания записи',
        auto_now_add=True,
    )
    status = models.ForeignKey(
        'Status', on_delete=models.DO_NOTHING,
        related_name='flows', verbose_name='Статус'
    )
    type = models.ForeignKey(
        'Type', on_delete=models.CASCADE,
        related_name='flows', verbose_name='Тип'
    )
    category = models.ForeignKey(
        'Category', on_delete=models.CASCADE,
        related_name='flows', verbose_name='Категория'
    )
    subcategory = models.ForeignKey(
        'Subcategory', on_delete=models.CASCADE,
        related_name='flows', verbose_name='Подкатегория'
    )
    amount = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name='Сумма'
    )
    comment = models.TextField(verbose_name='Комментарий', blank=True)


class Status(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True,
                            verbose_name='Название статуса')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Type(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True,
                            verbose_name='Название типа')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True,
                            verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    type = models.ForeignKey(
        Type,
        on_delete=models.CASCADE,
        related_name='categories',
        verbose_name='Тип'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Subcategory(models.Model):
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True,
                            verbose_name='Название подкатегории')
    slug = models.SlugField(unique=True, verbose_name='Слаг')

    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='subcategories',
        verbose_name='Категория'
    )

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name
