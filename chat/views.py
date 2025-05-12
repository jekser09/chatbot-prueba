from .mubot import Mubot 
from django.shortcuts import render
from django.http import JsonResponse

mubot=Mubot()

# Create your views here.
def chat(request):
    print(mubot.BIENVENIDA)
    return render(request,"index.html",{'msg':mubot.BIENVENIDA})

def conversacion(request,texto:str):
    front={'estado':False,'error':''}
    if request.method=='GET':
        front['respuesta']=mubot.responder(texto)
        front['estado']=True
    else: front['error']='Este metodo no esta permitido'
    return JsonResponse(front)
        


