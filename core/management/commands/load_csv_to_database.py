import csv
from datetime import date
from django.conf import settings 
from django.core.management.base import BaseCommand
from commodities.models import CommoditiesPrices



class Command (BaseCommand):
    help = 'Load data from precos_commodities.csv file'
    
    def handle(self, *args, **kwargs):
        datafile = settings.BASE_DIR / 'commodities' / 'data' / 'precos_commodities.csv'
        
        with open(datafile, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')
            
            for row in reader:
                dt = row['data'].split('/')
                dt = date(int(dt[2]), int(dt[1]), int(dt[0]))
                
                CommoditiesPrices.objects.get_or_create(
                    ativo=row['ativo'],
                    preco_de_abertura=row['preco_de_abertura'],
                    maximo_do_dia=row['maximo_do_dia'],
                    minimo_do_dia=row['minimo_do_dia'],
                    preco_de_fechamento=row['preco_de_fechamento'],
                    preco_de_fechamento_ajustado=row['preco_de_fechamento_ajustado'],
                    data=dt,
                    volume=row['volume_negociado'],
                    codigo=row['codigo'],
                    moeda=row['moeda']
            )