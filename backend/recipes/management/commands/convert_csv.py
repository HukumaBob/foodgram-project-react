import logging
from csv import DictReader

from django.core.management.base import BaseCommand

from recipes.models import Ingredient

TABLES = {
    Ingredient: "ingredients.csv",
}


class Command(BaseCommand):
    help = "Loads data from ingredients.csv"

    def handle(self, *args, **kwargs):
        for model, csv in TABLES.items():
            # Open the CSV file
            with open(f"{csv}", encoding="utf-8") as file:
                reader = DictReader(file)
                for data in reader:
                    obj, created = model.objects.get_or_create(**data)
                    if created:
                        logging.info(
                            self.style.SUCCESS(f"Created {obj}")
                        )
                    else:
                        logging.warning(f"{obj} already exists")
