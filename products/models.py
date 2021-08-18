from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200, verbose_name="Категория")
    parent = models.ForeignKey("self", on_delete=models.CASCADE,
                               blank=True, null=True, verbose_name="Категория")

    class Meta:
        verbose_name = "Категирия "
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField(max_length=100, verbose_name="Тег")

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.name


class Product(models.Model):
    title = models.CharField(max_length=100, verbose_name="Продукт")
    description = models.TextField(verbose_name="Описание")
    price = models.FloatField(verbose_name="Цена")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="Категория")
    tags = models.ManyToManyField(Tag, blank=True, verbose_name="Теги")

    class Meta:
        verbose_name = "Продукт "
        verbose_name_plural = "Продукты "

    def __str__(self):
        return self.title


class Review(models.Model):
    text = models.TextField(max_length=100, verbose_name="Обзор")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")

    class Meta:
        verbose_name = "Обзор "
        verbose_name_plural = "Обзоры "

    def __str__(self):
        return self.text
