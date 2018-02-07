from django import template
register = template.Library()

@register.filter(name='verificaLista')
def verificaLista(id, lista):
    retorno = False
    for aluno in lista:
        if aluno.id == id:
            retorno = True
            break
    else:
        retorno = False
    return retorno
