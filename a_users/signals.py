from django.contrib.auth.models import User  # Importe o modelo de usuário padrão do Django
from django.db.models.signals import post_save
from django.dispatch import receiver
from allauth.account.signals import user_signed_up
from .models import CustomProfile  # Importe o modelo CustomProfile ou substitua pelo seu modelo de perfil de usuário

# Este é um exemplo de como criar um perfil de usuário após a criação do usuário usando sinais do Django Allauth

@receiver(post_save, sender=User)  # Usamos o sinal post_save do Django para o modelo User
def create_user_profile(sender, instance, created, **kwargs):
    """
    Função para criar um CustomProfile sempre que um novo usuário é criado.
    """
    if created:
        CustomProfile.objects.create(user=instance)

@receiver(user_signed_up)  # Usamos o sinal user_signed_up fornecido pelo Django Allauth
def populate_profile_on_signup(request, user, **kwargs):
    """
    Função para popular o perfil do usuário quando o usuário se registra.
    Aqui você pode definir quaisquer campos adicionais do CustomProfile
    que deseja preencher com base nos dados fornecidos durante o registro.
    """
    # Exemplo: definindo o nome de exibição do usuário no perfil
    user.profile.display_name = user.username
    user.profile.save()  # Salve o perfil do usuário
