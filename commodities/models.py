from django.db import models

# Create your models here.
class CommoditiesPrices(models.Model):
        
    ativo = models.CharField(max_length=100)
    preco_de_abertura = models.FloatField()
    maximo_do_dia = models.FloatField()
    minimo_do_dia = models.FloatField()
    preco_de_fechamento = models.FloatField()
    preco_de_fechamento_ajustado = models.FloatField()
    data = models.DateField()
    volume = models.IntegerField()
    codigo = models.CharField(max_length=6)
    moeda = models.CharField(max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Commodities Price'
        verbose_name_plural = 'Commodities Prices'
        ordering = ['ativo', 'data']

    def __str__(self):
        return self.ativo
    