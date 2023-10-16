from django.db import models
from django.core.files import File
from PIL import Image
from io import BytesIO

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

    def process_uploaded_image(self, image):
        img = Image.open(image)
        img = img.convert('RGB')  # Converta a imagem para o modo RGB

        # Redimensione a imagem, se necessário
        img.thumbnail((300, 300))

        thumb_io = BytesIO()
        img.save(thumb_io, format='JPEG', quality=100)  # Salve a imagem como JPEG

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail

    def save(self, *args, **kwargs):
        if self.image:
            # Verifique a extensão do arquivo e processe de acordo (JPG ou PNG)
            if not self.image.name.endswith('.jpg') and not self.image.name.endswith('.jpeg'):
                self.image = self.process_uploaded_image(self.image)

        super().save(*args, **kwargs)

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.process_uploaded_image(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return 'https://via.placeholder.com/300x300'
