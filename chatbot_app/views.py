# chatbot_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import requests
import json


CHATBOT_API_URL = settings.CHATBOT_API_URL
CHATBOT_API_SHARED_SECRET = getattr(settings, 'CHATBOT_API_SHARED_SECRET', None)



def chatbot_interface_view(request):
    return render(request, 'chatbot_app/chat_interface.html')

@csrf_exempt
def send_chatbot_message_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message', '')

            if not user_message.strip():
                return JsonResponse({'error': 'A mensagem não pode ser vazia.'}, status=400)

            headers = {'Content-Type': 'application/json'}
            
            if CHATBOT_API_SHARED_SECRET:
                
                headers['X-API-Key'] = CHATBOT_API_SHARED_SECRET
            
                
            
            
            api_payload = {'question': user_message}
            
            response_from_api = requests.post(CHATBOT_API_URL, json=api_payload, headers=headers, timeout=180)
            response_from_api.raise_for_status()

            api_data = response_from_api.json()
            chatbot_answer = api_data.get('answer', 'Desculpe, não consegui processar sua pergunta no momento.')

            return JsonResponse({'user_message': user_message, 'chatbot_answer': chatbot_answer})

        except requests.exceptions.Timeout:
            return JsonResponse({'error': 'O assistente demorou muito para responder. Tente novamente.'}, status=504)
        except requests.exceptions.RequestException as e:
            print(f"Erro ao chamar API do chatbot: {e}") 
            return JsonResponse({'error': f'Ocorreu um erro ao contatar o assistente.'}, status=500)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de requisição inválido.'}, status=400)
        except Exception as e:
            print(f"Erro inesperado na view do chatbot: {e}")
            return JsonResponse({'error': 'Ocorreu um erro inesperado.'}, status=500)
    
    return JsonResponse({'error': 'Método não permitido.'}, status=405)