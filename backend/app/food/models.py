from django.db import models


class Tag(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='tag',
        unique=True,
        default='-',
    )
    color = models.CharField(max_length=7)
    slug = models.SlugField(
        max_length=255,
        unique=True,
        db_index=True,
        verbose_name="URL"
    )

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"
        ordering = ['name']

    def __str__(self):
        return self.name


class Ingredients(models.Model):
    name = models.CharField(
        max_length=20,
        verbose_name='Наименование',
        unique=True,
        null=False,
    )
    measurement_unit = models.ForeignKey(
        'Measurement_units',
        on_delete=models.PROTECT
    )

    class Meta:
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ['pk']

    def __str__(self):
        return self.name


class Measurement_units(models.Model):
    name = models.CharField(
        max_length=5,
        verbose_name='Единица',
        unique=True,
        null=False,
    )

    class Meta:
        verbose_name = "Единица измерения"
        verbose_name_plural = "Единицы измерения"
        ordering = ['pk']

    def __str__(self):
        return self.name
