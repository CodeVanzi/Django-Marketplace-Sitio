import pandas as pd
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Transform csv to json file'

    def handle(self, *args, **kwargs):
        csv_file = settings.BASE_DIR / 'commodities' / 'data' / 'precos_commodities.csv'
        commodities_df = pd.read_csv(csv_file, sep=';')
        commodities_df['data'] = pd.to_datetime(commodities_df['data'], format='%d/%m/%Y')
        
        # Convertendo a coluna de data para o formato desejado (YYYY-MM-DD)
        commodities_df['data'] = commodities_df['data'].dt.strftime('%Y-%m-%d')
        
        json_output = settings.BASE_DIR / 'commodities' / 'data' / 'precos_commodities.json'
        commodities_df.to_json(json_output, orient='records', indent=1)

