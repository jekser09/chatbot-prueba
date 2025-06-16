import random
from chat.dbctrl import Bot_db
import spacy
from spacy.training import Example
from spacy.util import minibatch, compounding

'''
comando para descargar idioma español en spacy
python -m spacy download es_core_news_md
'''

class Trainer():

    def __init__(self,ruta):
        self.__ruta_modelo=ruta
        self.__word='cats' #Frase estandar para el dataset de entrenamiento
        self.__nlp=spacy.load("es_core_news_md") #Modelo en español preentrenado para enteder el idioma
        self.__textcat=self.__nlp.add_pipe('textcat',last=True)
        with Bot_db() as db:
            '''consultas en la base de datos'''
            respuesta=db.get_frases()
        if respuesta['estado']:
            self.__frases_intenciones=respuesta['data']
            self.__ajuste_intenciones(self.__frases_intenciones)
            self.__ajuste_dataset(self.__frases_intenciones)
            self.__entrenamiento()
    
    def __ajuste_intenciones(self,frases_inteciones:list)->list:
        intenciones=[]
        for x in frases_inteciones:
            intenciones.append(x[1:3])
        self.__intenciones=dict(set(intenciones))
        self.__etiquetas=list(self.__intenciones.values())
    
    def __ajuste_dataset(self,frases_inteciones:list)->list:
        self.__examples=[]
        for data in frases_inteciones:
            aux_intenciones={}
            frase=data[3]
            for key in self.__intenciones:
                if self.__intenciones[key]==data[2]:
                    aux_intenciones[self.__intenciones[key]]=True
                else:
                    aux_intenciones[self.__intenciones[key]]=False
            doc=self.__nlp.make_doc(frase)
            ejemplo=Example.from_dict(doc,{self.__word:aux_intenciones})
            self.__examples.append(ejemplo)

    def __entrenamiento(self,iteraciones=15):
        for etiqueta in self.__etiquetas: self.__textcat.add_label(etiqueta)
        optimizer=self.__nlp.begin_training()
        for iteracion in range(iteraciones):
            random.shuffle(self.__examples)
            batches=minibatch(self.__examples,size=compounding(4.0,32.0,1.001))
            for batch in batches:
                self.__nlp.update(batch,sgd=optimizer)
        self.__nlp.to_disk(self.__ruta_modelo)

    def get_intenciones(self): return self.__intenciones

    def get_etiquetas(self): return self.__etiquetas
