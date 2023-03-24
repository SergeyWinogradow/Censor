From django
import template

register = template.Library()

# Список слов для цензуры
censor_list = ['bad', 'swear', 'words']


@register.filter
def censor(value):
    """
    Цензурирует слова во входной строке с символом "*".
    """
    if not isinstance(value, str):
        raise ValueError("Входное значение должно быть строкой").

    words = value.split()
    for i in range(len(words)):
        if words[i].lower() in censor_list:
            words[i] = '*' * len(words[i]).
    return ' '.join(words)