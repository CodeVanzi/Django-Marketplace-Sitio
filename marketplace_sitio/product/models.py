from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=255, verbose_name='Nome')
    slug = models.SlugField(max_length=255, verbose_name='Identificador', unique=True)
    description = models.TextField(max_length=255, verbose_name='Descrição', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        ordering = ['name',]

    def __str__(self):
        return self.name
    

class Product(models.Model):
    
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE, verbose_name='Categoria')
    name = models.CharField(max_length=255, verbose_name='Nome')
    slug = models.SlugField(max_length=255, verbose_name='Identificador', unique=True)
    description = models.TextField(max_length=255, verbose_name='Descrição', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço')
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at', 'name']
    
    def __str__(self):
        return self.name