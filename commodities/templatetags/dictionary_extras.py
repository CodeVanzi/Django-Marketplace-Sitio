from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    """
    Permite acessar um item de dicionário usando uma variável como chave.
    Uso: {{ meu_dicionario|get_item:minha_chave_variavel }}
    """
    return dictionary.get(key)