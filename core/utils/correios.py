import requests

def validar_cep(cep):
    # URL da API dos Correios para consulta de CEPs
    url = f"http://viacep.com.br/ws/{cep}/json/"
    
    try:
        # Fazendo a requisição GET para a API dos Correios
        response = requests.get(url)
        # Verifica se a requisição foi bem sucedida
        if response.status_code == 200:
            # Converte a resposta para JSON
            data = response.json()
            # Verifica se o CEP é válido
            if 'erro' in data:
                return False
            else:
                return True
        else:
            # Caso a requisição falhe, retorna False
            return False
    except requests.exceptions.RequestException as e:
        # Em caso de erro na requisição, retorna False
        print(f"Erro na consulta de CEP: {e}")
        return False