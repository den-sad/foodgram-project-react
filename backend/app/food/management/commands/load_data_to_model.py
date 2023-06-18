import json
from django.core.management.base import BaseCommand
from food.models import Ingredients, Tag


class Command(BaseCommand):
    help = "Загрузка ингредиентов из файла b начальное заполнение"

    def add_arguments(self, parser):
        parser.add_argument('model', type=str, help='Модель для загрзуки')
        parser.add_argument('-f', '--file', type=str,
                            help='Имя файла данных', )

    def handle(self, *args, **kwargs):
        model = kwargs['model']
        filename = kwargs['file']
        print(f'Загрузка в таблицу модели {model}')
        if model == 'Ingredients':
            with open(filename, encoding='utf-8', newline='') as jsonfile:
                data = json.load(jsonfile,)
                for el in data:
                    ingridient, _ = Ingredients.objects.get_or_create(
                        name=el['name'],
                        measurement_unit=el['measurement_unit']
                    )
                    print(f'Обработан ингредиент: {ingridient}')

        if model == 'Tags':
            tag, _ = Tag.objects.get_or_create(
                name='Dinner',
                color='#FF0000',
                slug='diner'
            )
            tag, _ = Tag.objects.get_or_create(
                name='Lunch',
                color='#00FF00',
                slug='lunch'
            )
            tag, _ = Tag.objects.get_or_create(
                name='Breakfast',
                color='#0000FF',
                slug='breakfast'
            )
            print('Обработаны тэги: Dinner, Lunch, Breakfast')
