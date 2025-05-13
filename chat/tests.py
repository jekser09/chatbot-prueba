from dbctrl import Bot_db
from nlp.bot_trainer import Trainer
from nlp.bot_predictor import Predictor
from mubot import Mubot
from django.test import TestCase

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
    productos_bd=productos['data']
    productos_dict = {
        nombre: (id_prod, nombre, precio)
        for id_prod, nombre, precio in productos_bd
    }
    while True:
        texto=input('pregunta: ')
        texto=texto.upper()
        for nombre_producto in productos_dict:
            if nombre_producto in texto:
                print(productos_dict[nombre_producto])

def prueba_string_productos():
    consultas=[]
    text='quiero comprar queso crema y mantequilla clarificada o queso consteno'
    text=text.upper()
    if ' Y ' in text:
        aux_tex=text.split(' Y ')
        consultas+=aux_tex
    for tex in consultas:
        if ' O ' in tex:
            aux_tex=text.split(' O ')

if __name__=='__main__':
    #prueba_entrenamiento()
    #prueba_modelo()
    precision_modelo()
    #productos()
    #palabras_productos()
    #prueba_string_productos()