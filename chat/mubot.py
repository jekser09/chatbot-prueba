import random
import locale
from dbctrl import Bot_db
from nlp.bot_predictor import Predictor
from nlp.bot_trainer import Trainer
from rapidfuzz import fuzz

class Mubot:

    def __init__(self):
        self.__predictor=Predictor()
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
            aux=['Si tenemos: ']
            # ordenamos por score descendente
            encontrados.sort(key=lambda x: x[3], reverse=True)
            return aux+encontrados
        
        # --- Si no hay match fuerte, buscar por palabra clave ---
        # extraer keyword (ej. "queso")
        posibles = [(0,'No encontre el producto que querias pero te recomiendo estos: ',0)]
        for id_prod, nombre_prod, precio in self.__productos:
            if any(palabra in nombre_prod.lower() for palabra in texto_usuario.split()):
                posibles.append((id_prod, nombre_prod, precio, 0))  # score 0 = sugerencia
        if not len(posibles)==1:
            posibles=[(0,'No tenemos el producto que solicitas :(',0)]
        return posibles

    def responder(self,texto:str)->list:
        intencion=self.__predictor.predecir_intencion(texto)
        if intencion[1] >= self.__predictor.UMBRAL:
            print(f'-----------------intencion: {intencion}---------------------')
            msjs=self.__predictor.get_mensajes().get(intencion[0])
            if isinstance(msjs,str):
                return [msjs]
            elif isinstance(msjs,bool):
                return self.__buscar_productos(texto)
            else:
                return [random.choice(msjs)]
        else: return [self.__predictor.get_mensajes().get('ERROR')]
    
    def entrenar_modelo(self):
        print("Entrenando...")
        Trainer(ruta="nlp/mubot_modelo")
        print("Entrenamiento completado.")