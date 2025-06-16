from django.http import JsonResponse,HttpResponseNotFound
from django.shortcuts import render,redirect
from .forms import form_login
from .dbctrl import sql_usuarios
from core.decorators import restringir_login,validar_login
from django.views.decorators.cache import never_cache

@never_cache
@restringir_login
def login(request):
    '''Logica de inicion de sesion de los usuarios'''
    front = {"form":form_login}
    if request.method == "POST":
        form = form_login(request.POST)
        if form.is_valid():
            #Busca el usuario en la BD
            with sql_usuarios() as db:
                r_db = db.login(form.cleaned_data['usuario'],clave = form.cleaned_data['clave'])
            if r_db['estado']:
                if r_db['data']['lista_menus']:
                    # --- Guardar los datos del usuario en la sesión ---
                    for dato in r_db['data']: request.session[dato]=r_db['data'][dato]
                    return redirect('menu_general') # Redirige al menú principal del usuario
            else: front['errordb'] = r_db.get('error', 'Error de base de datos.')
        else: front['form']=form
        return render(request,"index.html",front)
    elif request.method == "GET":
        return render(request,"index.html",front)
    else: return HttpResponseNotFound

@validar_login
def menu_general(request):
    return render(request,"menu_usuarios.html",{'menu':'principal'})


def probar_db(request):
    if request.method=="GET":
        with sql_usuarios() as db:
            return JsonResponse(db.estado_db())
    return HttpResponseNotFound

def logout(request):
    '''Elimina los datos de sesion de las cookies'''
    request.session.flush()
    return redirect('index')
