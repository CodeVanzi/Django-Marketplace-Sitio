from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Função para criar um CustomProfile sempre que um novo usuário é criado.
    """
    if created:
        user = instance
        email = instance.email  # Acesso ao e-mail do usuário
        nickname = f'{instance.first_name} {instance.last_name}'  # Criação de um apelido
        
        profile = CustomProfile.objects.create(user=user, email=email, nickname=nickname)


