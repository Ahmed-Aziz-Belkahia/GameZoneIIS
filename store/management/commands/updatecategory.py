from django.core.management.base import BaseCommand
from store.models import Category
import pandas as pd

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass
    
    def handle(self, *args, **options):
        df = pd.read_csv('categories.csv')
        for id, name in zip(df.term_id, df.name):
            category = Category(
                id=id,
                title=name
            )
            category.save()