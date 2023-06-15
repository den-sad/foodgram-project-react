import json
from django.core.management.base import BaseCommand, CommandError
from food.models import Ingredients


class Command(BaseCommand):
    help = "Загрузка ингредиентов из файла"

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
                    print(el)

                    # unit, created = Measurement_units.objects.get_or_create(
                    #     name=el['measurement_unit'])
                    ingridient, created = Ingredients.objects.get_or_create(
                        name=el['name'],
                        measurement_unit=el['measurement_unit']
                    )
                    print(f'created = {created}')
                    print(ingridient)
