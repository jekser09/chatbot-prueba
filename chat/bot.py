import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.data import find

class botest():
    def __init__(self):
        self._SALUDOS_INPUTS = ("hola", "buenas", "saludos", "qué tal", "hey","buenos dias",)
        self._SALUDOS_OUTPUTS = ["Hola", "Hola, ¿Qué tal?", "Hola, ¿Cómo te puedo ayudar?", "Hola, encantado de hablar contigo"]
        self._recursos={'punkt':False,'wordnet':False,'stopwords':False,'punk_tab':False}
        self._status_bot={"estado":False,"msg":""}
        self._saludo_inicial=""
        try:
            self.instalacion_recursos()
            with open(r"chat/static/corpus/Corpus_crucero.txt","r",errors='ignore') as file:
                self._raw=file.read()
            self._status_bot["estado"]=True
            self._status_bot["msg"]+="Configuraciones del bot correctas\n"
            self.preprocesamiento_txt()
        except Exception as e:
            self._status_bot["msg"]+=f"Error al cargar corpus >>> {e}\n"
        

    def __str__(self):
        return self._status_bot['msg']

    def instalacion_recursos(self):
        print("Verificando recursos...\n")
        for rec in self._recursos:
            if not self._recursos[rec]:
                try:
                    # Verificar si el recurso ya está instalado
                    find(rec)
                    self._recursos[rec] = True
                    print(f"✓ Recurso '{rec}' ya instalado.")
                except LookupError:
                    # Si no está instalado, intentar descargarlo
                    print(f"⚡ Recurso '{rec}' no encontrado. Descargando...")
                    try:
                        nltk.download(rec)
                        self._recursos[rec] = True
                        print(f"✔ Recurso '{rec}' descargado exitosamente.\n")
                    except Exception as e: pass

        # Verificar si todos los recursos se instalaron
        if all(self._recursos.values()):
            self._status_bot["estado"]=True
            self._status_bot["msg"]+="Todos los recursos fueron instalados correctamente\n"
        else:
            faltantes = [r for r, estado in self._recursos.items() if not estado]
            self._status_bot["estado"]=False
            self._status_bot["msg"]+="Recursos faltantes: {', '.join(faltantes)}\n"

    def preprocesamiento_txt(self):
        self._raw=self._raw.lower()# convertir en minúscula
        self._sent_tokens = nltk.sent_tokenize(self._raw)# Convierte el CORPUS a una lista de sentencias
        self._word_tokens = nltk.word_tokenize(self._raw)# Convierte el CORPUS a una lista de palabras

    #WordNet diccionario semántico incluido en NLTK
    def LemTokens(self,tokens):
        self._lemmer = nltk.stem.WordNetLemmatizer()
        return [self._lemmer.lemmatize(token) for token in tokens]

        
    def LemNormalize(self,text):
        remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
        return self.LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

    #Función para determinar la similitud del texto insertado y el corpus
    def response(self,user_response):
        robo_response=''
        self._sent_tokens.append(user_response) #Añade al corpus la respuesta de usuario al final
        TfidfVec = TfidfVectorizer(tokenizer=self.LemNormalize, stop_words=stopwords.words('spanish'))
        tfidf = TfidfVec.fit_transform(self._sent_tokens)
        # 3 EVALUAR SIMILITUD DE COSENO ENTRE MENSAJE USUARIO (tfidf[-1]) y el CORPUS (tfidf)
        vals = cosine_similarity(tfidf[-1], tfidf)
        idx=vals.argsort()[0][-2]
        flat = vals.flatten()
        flat.sort()
        req_tfidf = flat[-2]
        
        if(req_tfidf==0):
            robo_response=robo_response+"Lo siento, no te he entendido. Si no puedo responder a lo que busca póngase en contacto con soporte@soporte.com"
            return robo_response

        else:
            robo_response = robo_response+self._sent_tokens[idx]
            return robo_response

    def saludos(self,sentence):
        for word in sentence.split():
            if word.lower() in self._SALUDOS_INPUTS:
                return random.choice(self._SALUDOS_OUTPUTS)

    def bucle_principal(self) -> str:
        if not self._status_bot['estado']:
            return '''
            Lo siento no estoy configurado correctamente aun contacta con
            soporte@soporte.com para socluionar este incoveniente :(
            '''
        if self._saludo_inicial=="":
            return '''
            Bienvenido Mi nombre es MUUU-BOT.
            Contestaré a tus preguntas acerca de tus vacaciones
            en el crucero.
            estare encantado de ayudarte
            '''
        while True:
            user_response = input()
            user_response = user_response.lower() #Convertimos a minúscula
            
            if(user_response!='salir'):
                if(user_response=='gracias' or user_response=='muchas gracias'): #Se podría haber definido otra función de coincidencia manual
                    print("ROBOT: No hay de qué")
                else:
                    if(self.saludos(user_response)!=None): #Si la palabra insertada por el usuario es un saludo (Coincidencias manuales definidas previamente)
                        print("ROBOT: "+self.saludos(user_response))
                    else: #Si la palabra insertada no es un saludo --> CORPUS
                        print("ROBOT: ",end="") 
                        print(self.response(user_response))
                        self._sent_tokens.remove(user_response) # para eliminar del corpus la respuesta del usuario y volver a evaluar con el CORPUS limpio
            else:
                print("ROBOT: Nos vemos pronto, ¡cuídate!")
                break