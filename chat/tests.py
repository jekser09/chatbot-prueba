from dbctrl import Bot_db
from nlp.bot_trainer import Trainer
from nlp.bot_predictor import Predictor
from mubot import Mubot
from django.test import TestCase

text='quiero comprar queso crema'
tokenizado=['queso','crema']
productos=['queso crema x algo']

# Create your tests here.
def prueba_entrenamiento():
    print('Entrenando...')
    Trainer(ruta='chat/nlp/mubot_modelo')
    print('Entrenamiento completo...')

def prueba_modelo():
    try:
        mubot=Mubot()
        while True:
            doc=mubot.responder(input("Texto:"))
            for x in doc:
                print(x)
            #intencion = max(doc.cats, key=doc.cats.get)
            #print(f"Intención detectada: {intencion}")
            print('----------------------------- press ctrl+c para terminar')
    except KeyboardInterrupt: print('Saliendo...')

def precision_modelo():
    predictor=Predictor()
    print(predictor.get_precision())

def productos():
    with Bot_db() as db:
        productos=db.get_productos()
    print(productos)
    try:
        while True:
            respuestas=[]
            texto=input('Texto: ')
            for producto in productos['data']:
                if texto.upper() in producto[1]:
                    respuestas.append(producto)
            if respuestas:
                for x in respuestas: print(x)
            else:
                print(f'Aun no tenemos ese producto, pero lo tendremos pronto :D')
    except KeyboardInterrupt:
        print('saliendo')

def palabras_productos():
    with Bot_db() as db:
        productos=db.get_productos()
    palabras=[]
    for producto in productos['data']:
        aux=producto[1].split()
        for palabra in aux:
            if len(palabra)>3 and not palabra.isnumeric():
                if 'APROX' in palabra: continue
                if 'TIPO' in palabra: continue
                if '(' in palabra: palabra=palabra.replace('(','')
                if ')' in palabra: palabra=palabra.replace(')','')
                palabras.append(palabra)   
    print(set(palabras))
if __name__=='__main__':
    #prueba_entrenamiento()
    prueba_modelo()
    #precision_modelo()
    #productos()
    #palabras_productos()