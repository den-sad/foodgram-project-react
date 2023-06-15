from django.db import models
from django.conf import settings


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
        unique=False,
        null=False,
    )
    measurement_unit = models.CharField(
        max_length=20,
        verbose_name='Единица измерения',
        unique=False,
        null=False,
    )

    class Meta:
        unique_together = ('name', 'measurement_unit',)
        verbose_name = "Ингридиент"
        verbose_name_plural = "Ингридиенты"
        ordering = ['pk']

    def __str__(self):
        return self.name


class Recipes(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор'
    )
    name = models.CharField(
        max_length=250,
        verbose_name='Название',
        null=False,
    )
    image = models.ImageField(
        upload_to='recipes/images/',
        null=True,
        default=None
    )
    text = models.TextField()

    cooking_time = models.IntegerField(
        blank=False,
    )
    ingredients = models.ManyToManyField(
        Ingredients,
        through='RecipeIngredients',
        related_name='recipes',
    )
    tags = models.ManyToManyField(
        Tag,
        through='RecipeTags',
        related_name='recipes',
    )

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"
        ordering = ['-pk']

    def __str__(self):
        return self.name


class RecipeIngredients(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE)
    amount = models.FloatField()

    def __str__(self):
        return f'{self.recipe} {self.ingredient}'


class RecipeTags(models.Model):
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE)
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('recipe', 'tags',)

    def __str__(self):
        return f'{self.recipe} {self.tags}'
