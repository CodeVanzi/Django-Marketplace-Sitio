import csv
from django.conf import settings 
from django.core.management.base import BaseCommand
from commodities.models import MediasCommodities



class Command (BaseCommand):
    help = 'Load data from medias.csv file'
    
    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'commodities' / 'data' / 'medias.csv'
        
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=',')
            
            for row in reader:               
                MediasCommodities.objects.get_or_create(
                ativo = row['ativo'],
                media_ult_ano = row['media_ult_ano'],
                media_ult_sem = row['media_ult_sem'],
                media_ult_tri = row['media_ult_tri'],
                media_ult_mes = row['media_ult_mes'],
                variacao_ano = row['variacao_ano'],
                variacao_sem = row['variacao_sem'],
                variacao_tri = row['variacao_tri'],
                variacao_mes = row['variacao_mes']
            )