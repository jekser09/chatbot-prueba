import random
import locale
from dbctrl import Bot_db
from nlp.bot_predictor import Predictor
from nlp.bot_trainer import Trainer
from spacy.util import minibatch, compounding

class Mubot:

    def __init__(self):
        self.__predictor=Predictor()
        self.__cargar_productos()
        self.__palabras_productos()
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')  # para Linux/mac
    
    def __cargar_productos(self)->None:   
        with Bot_db() as db:
            productos=db.get_productos()
        if productos['estado']:
            self.__productos=productos['data']
        else:
            self.__productos=[]
    
    def __palabras_productos(self,)->None:
        palabras=[]
        for producto in self.__productos:
            aux=producto[1].split()
            for palabra in aux:
                if len(palabra)>3 and not palabra.isnumeric():
                    if 'APROX' in palabra: continue
                    if 'TIPO' in palabra: continue
                    if '(' in palabra: palabra=palabra.replace('(','')
                    if ')' in palabra: palabra=palabra.replace(')','')
                    palabras.append(palabra)   
        self.__palabras_str=list(set(palabras))

    def __buscar_producto(self,texto:str)->list:
        respuesta=['Si tenemos: ']
        token_texto=texto.upper().split()
        productos_busqueda=list(filter(lambda x: x in self.__palabras_str,token_texto))
        if productos_busqueda:
            if not self.__productos: return 'No tenemos productos :('
            for producto in self.__productos:
                for produser in productos_busqueda:
                    if produser in producto[1]:
                        respuesta.append(f"{producto[1]} y cuesta{locale.currency(producto[2],symbol=True,grouping=True)}")
        return respuesta

    def responder(self,texto:str)->list:
        intencion=self.__predictor.predecir_intencion(texto)
        if intencion[1] >= self.__predictor.UMBRAL:
            print(f'-----------------intencion: {intencion}---------------------')
            msjs=self.__predictor.get_mensajes().get(intencion[0])
            if isinstance(msjs,str):
                return [msjs]
            elif isinstance(msjs,bool):
                return self.__buscar_producto(texto)
            else:
                return [random.choice(msjs)]
        else: return [self.__predictor.get_mensajes().get('ERROR')]
    
    def entrenar_modelo(self):
        print("Entrenando...")
        Trainer(ruta="nlp/mubot_modelo")
        print("Entrenamiento completado.")