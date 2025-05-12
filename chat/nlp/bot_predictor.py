import json
import spacy
from sklearn.metrics import classification_report

class Predictor:

    def __init__(self):
        self.UMBRAL=0.70
        self.__nlp=spacy.load('chat/nlp/mubot_modelo')
        with open('chat/nlp/set_pruebas.json','r') as fjson:
            self.__pruebas=json.load(fjson)
    
    def predecir_intencion(self,texto:str):
        doc=self.__nlp(texto)
        intencion=max(doc.cats,key=doc.cats.get)
        confianza=doc.cats[intencion]
        return intencion,confianza
    
    def get_precision(self)->str:
        y_true,y_pred=[],[]
        for texto,intencion in self.__pruebas['preguntas']:
            doc=self.__nlp(texto)
            prediccion=max(doc.cats,key=doc.cats.get)
            y_true.append(intencion)
            y_pred.append(prediccion)
        return classification_report(y_true,y_pred)
    
    def get_mensajes(self)->dict:
        try:
            with open('chat/nlp/bot_msgs/msgs.json','r',encoding="utf-8") as fjson:
                return json.load(fjson)
        except FileNotFoundError as fe:
            return {'error':f'No existe el archivo msgs.json: {fe}'}