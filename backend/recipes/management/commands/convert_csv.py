import logging
from csv import DictReader

from django.core.management.base import BaseCommand
from recipes.models import Ingredient

# Dictionary mapping models to their corresponding CSV files
TABLES = {
    Ingredient: "ingredients.csv",
}


class Command(BaseCommand):
    # Show this when the user types help
    help = "Loads data from ingredients.csv"

    def handle(self, *args, **kwargs):
        # Iterate over the models and their respective CSV files
        for model, csv in TABLES.items():
            # Open the CSV file
            #with open(f"./data/{csv}", encoding="utf-8") as file:
            with open(f"{csv}", encoding="utf-8") as file:
                # Create a dictionary reader for the CSV file
                reader = DictReader(file)
                # Iterate over each row in the CSV file
                for data in reader:
                    # Get or create an object of the current model using the row data
                    obj, created = model.objects.get_or_create(**data)
                    # Check if the object was newly created or already existed
                    if created:
                        logging.info(self.style.SUCCESS(f"Created {obj}"))
                    else:
                        logging.warning(f"{obj} already exists")
