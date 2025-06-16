from .mubot import Mubot 
from django.shortcuts import render
from django.http import JsonResponse
from core.decorators import validar_login

mubot=Mubot()

@validar_login
def chat(request):
    print(mubot.BIENVENIDA)
    return render(request,"chatbot.html",{'msg':mubot.BIENVENIDA})

def conversacion(request,texto:str):
    front={'estado':False,'error':''}
    if request.method=='GET':
        front['respuesta']=mubot.responder(texto)
        front['estado']=True
    else: front['error']='Este metodo no esta permitido'
    return JsonResponse(front)

def estadisticas(request):
    front={'estado':False,'error':''}
    if request.method=='GET':
        try:
            front['respuesta']=mubot.estadisticas_modelo()
            front['estado']=True
        except Exception as e:
            front['error']=e
    return JsonResponse(front)
        


