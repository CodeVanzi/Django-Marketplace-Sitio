from django.urls import path
from . import views

app_name = 'chatbot_app' # Define o namespace da aplicação, útil para {% url %}

urlpatterns = [
    # URL para a interface principal do chat
    # Ex: /assistente-virtual/
    path('', views.chatbot_interface_view, name='chat_interface'), 
    
    # URL para a API interna do Django que recebe a mensagem do usuário e chama a API Flask
    # Ex: /assistente-virtual/send_message/
    path('send_message/', views.send_chatbot_message_view, name='send_message_api'),
]