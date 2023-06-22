from colorfield.fields import ColorField
from django.db import models
from django.conf import settings
from django.core.validators import RegexValidator


class Tag(models.Model):
    '''Тэги применяемые к рецептам'''
    COLOR_PALETTE = [
        ("#FFFFFF", "white", ),
        ("#000000", "black", ),
    ]

    name = models.CharField(
        max_length=20,
        verbose_name='tag',
        unique=True,
    )
    color = ColorField(
        default='#FF0000',
        samples=COLOR_PALETTE,
        max_length=7,
        validators=[RegexValidator(
            regex='^#([0-9a-fA-F]{3}){1,2}$',
            message='Неверный цвет HEX (#AABBCC)',
        ),
        ]
    )
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
    '''Ингридиенты применяемые в рецептах'''
    name = models.CharField(
        max_length=200,
        verbose_name='Наименование',
        unique=False,
        null=False,
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        unique=False,
        null=False,
    )

    class Meta:
        unique_together = ('name', 'measurement_unit',)
        verbose_name = "Ингрeдиент"
        verbose_name_plural = "Ингрeдиенты"
        ordering = ['pk']

    def __str__(self):
        return f'{self.name}, {self.measurement_unit}'


class Recipes(models.Model):
    '''Модель рецептов, связана с тэгами и ингридиентами
    по типу многие ко многим'''
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

    cooking_time = models.PositiveSmallIntegerField(
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
    '''Модель для свзяи рецепта и ингридиента'''
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='recipeingredient')
    ingredient = models.ForeignKey(Ingredients, on_delete=models.CASCADE,
                                   related_name='recipeingredient')
    amount = models.FloatField()

    class Meta:
        unique_together = ('recipe', 'ingredient',)
        verbose_name = 'Ингрeдиент в рецепте'
        verbose_name_plural = 'Ингрeдиенты в рецептах'

    def __str__(self):
        return f'В рецепте {self.recipe} заложен ингредиент {self.ingredient}'


class RecipeTags(models.Model):
    '''Модель для свзяи рецепта и тэга'''
    recipe = models.ForeignKey(Recipes, on_delete=models.CASCADE,
                               related_name='recipeitag')
    tags = models.ForeignKey(Tag, on_delete=models.CASCADE,
                             related_name='recipeitag')

    class Meta:
        unique_together = ('recipe', 'tags',)
        verbose_name = 'Тэг назначеный рецепту'
        verbose_name_plural = 'Тэги назначенные рецептам'

    def __str__(self):
        return f'Рецепту {self.recipe} присвоен тэг {self.tags}'
