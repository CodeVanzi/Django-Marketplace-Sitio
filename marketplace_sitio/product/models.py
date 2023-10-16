from django.db import models
from django.core.files import File

from PIL import Image
from io import BytesIO

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
    # price = models.IntegerField(verbose_name='Preço')
    image = models.ImageField(upload_to='products', verbose_name='Imagem', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='thumbnails', verbose_name='Miniatura', blank=True, null=True)
    
    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'
        ordering = ['-created_at', 'name']
    
    def __str__(self):
        return self.name
    
    # def get_display_price(self):
    #     return f'R$ {self.price}/100'
    
    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/240x240x.jpg?text=Sem+imagem'
            
    def make_thumbnail(self, image, size=(300, 300)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        
        thumbnail = File(thumb_io, name=image.name)
        
        return thumbnail