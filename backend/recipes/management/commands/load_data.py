import csv

from django.core.management import BaseCommand
from recipes.models import Ingredient, Tag


class Command(BaseCommand):
    help = 'Загрузка из csv файла'

    def handle(self, *args, **kwargs):
        print('Обработка файла ingredients.csv')
        with open(
            './recipes/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            Ingredient.objects.bulk_create(
                Ingredient(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Все ингридиенты загружены!'))

        print('Обработка файла tags.csv')
        with open(
            './recipes/data/tags.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.DictReader(file)
            Tag.objects.bulk_create(
                Tag(**data) for data in reader)
        self.stdout.write(self.style.SUCCESS('Все тэги загружены!'))
