from django import template
import re


register = template.Library()


BAD_WORDS = ['редиска', 'редиски']

@register.filter()
def censor(value):
   for word in BAD_WORDS:
        pattern = f'({word[0].upper()}|{word[0].lower()}){word[1:]}'
        value = re.sub(pattern, f'\\1{"*" * (len(word) - 1)}', value)

   return value