import random
import locale
from .dbctrl import Bot_db
from .nlp.bot_predictor import Predictor
from .nlp.bot_trainer import Trainer
from rapidfuzz import fuzz

class Mubot:

    def __init__(self):
        self.__predictor=Predictor()
        self.BIENVENIDA=self.__predictor.get_mensajes()['BIENVENIDA']
        self.__cargar_productos()
        locale.setlocale(locale.LC_ALL, 'es_CO.UTF-8')  # para Linux/mac
    
    def __cargar_productos(self)->None:   
        with Bot_db() as db:
            productos=db.get_productos()
        if productos['estado']:
            self.__productos=productos['data']
            self.__productos_dict = {
                nombre: (id_prod, nombre, precio)
                for id_prod, nombre, precio in self.__productos
            }
        else:
            self.__productos=[]
            self.__productos_dict={}

    def __buscar_productos(self,texto_usuario:str,umbral=55)->list:
        texto_usuario = texto_usuario.lower()
        encontrados = []
        # fuzzy match
        for id_prod, nombre_prod, precio in self.__productos:
            nombre_normalizado = nombre_prod.lower()
            score = fuzz.partial_ratio(nombre_normalizado, texto_usuario)
            if score >= umbral:
                encontrados.append((id_prod, nombre_prod, precio, score))
        
        if encontrados:
            aux='Claro que si, te ofresco:<br>'
            # ordenamos por score descendente
            encontrados.sort(key=lambda x: x[3], reverse=True)
            for x in encontrados:
                aux+=f'{x[1]} con un valor de {x[2]}, <br>'
            encontrados=aux
            return aux
        
        # --- Si no hay match fuerte, buscar por palabra clave ---
        # extraer keyword (ej. "queso")
        posibles = ['No encontre el producto que querias pero te recomiendo estos: <br>']
        for id_prod, nombre_prod, precio in self.__productos:
            if any(palabra in nombre_prod.lower() for palabra in texto_usuario.split()):
                posibles.append(f'{nombre_prod} con un valor de {precio}')  # score 0 = sugerencia
        print(posibles)
        if len(posibles)>1:
            aux=''
            for x in posibles:
                aux+=f'{x} <br>'
            posibles=posibles
        elif len(posibles)==1: posibles='No tenemos el producto que solicitas :('
        else: posibles="Disculpa no te he entendido. :("
        return posibles

    def responder(self,texto:str)->list:
        intencion=self.__predictor.predecir_intencion(texto)
        if intencion[1] >= self.__predictor.UMBRAL:
            print(f'-----------------intencion: {intencion}---------------------')
            msjs=self.__predictor.get_mensajes().get(intencion[0])
            if isinstance(msjs,str):
                return msjs
            elif isinstance(msjs,bool):
                return self.__buscar_productos(texto)
            else:
                return random.choice(msjs)
        else: return self.__predictor.get_mensajes().get('ERROR')
    
    def entrenar_modelo(self):
        Trainer(ruta="nlp/mubot_modelo")
        return 'Entrenado'
    
    def estadisticas_modelo(self):
        return self.__predictor.get_precision()
