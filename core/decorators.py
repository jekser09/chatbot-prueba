from django.shortcuts import redirect
from functools import wraps

def validar_login(vista_func):
    '''Este decorador valida si existe un usuario logeado, si no redirije al index'''
    @wraps(vista_func)
    def wrapper(request,*args,**kwargs):
        if 'usuario' not in request.session:
            return redirect("index")
        return vista_func(request,*args,**kwargs)
    return wrapper

#Decorador para validar que los usuarios que esten logeados no pueda acceder al login
def restringir_login(vista_func):
    '''Este decorador valida si existe un usuario logeado, si existe redirije al menu general'''
    def wrapper(request,*args,**kwargs):
        if "usuario" in request.session:
            return redirect("menu_general")
        return vista_func(request,*args,**kwargs)
    return wrapper