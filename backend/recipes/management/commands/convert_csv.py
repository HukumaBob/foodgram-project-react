import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import IntegrityError
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'CSV file download...'

    def handle(self, *args, **options):
        with open(
            f'{settings.BASE_DIR}/data/ingredients.csv',
            'r',
            encoding='utf-8'
        ) as csv_file:
            reader = csv.DictReader(csv_file)
            try:
                Ingredient.objects.bulk_create(
                    Ingredient(**items) for items in reader
                )
            except IntegrityError:
                return 'This ingredient is already exists'
        return (
            f'{Ingredient.objects.count()} - ingredients download')
