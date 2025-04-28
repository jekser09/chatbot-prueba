import nltk
import numpy as np
import random
import string
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
import json

class botest():
    def __init__(self):
        self._status_bot={"estado":False,"msg":""}
        try:
            self.instalacion_recursos()
            with open("chat/static/bot_msgs/msgs.json","r",encoding="utf-8") as filejson:
                self._textos=json.load(filejson)
            with open(r"chat/static/corpus/Corpus_lacteos.txt","r",errors='ignore') as file:
                self._raw=file.read()
            self._status_bot["estado"]=True
            self._status_bot["msg"]+="Configuraciones del bot correctas\n"
        except LookupError as le:
            self._status_bot["msg"]+=f"Error al instalar recursos {le}"
        except FileNotFoundError as fe:
            self._status_bot["msg"]+=f"Error al cargar textos {fe}"
        except Exception as e:
            self._status_bot["msg"]+=f"Error inesperado {e}\n"
        finally:
            self.preprocesamiento_txt()        

    def __str__(self):
        return self._status_bot['msg']

    def instalacion_recursos(self):
        print("Verificando recursos...\n")
        nltk.download("punkt")
        nltk.download("wordnet")
        nltk.download("punkt_tab")

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
            robo_response=robo_response+"Lo siento, no te he entendido. no puedo responder a lo que buscas ponte en contacto con soporte@soporte.com"
            return robo_response
        else:
            robo_response = robo_response+self._sent_tokens[idx]
            return robo_response

    def respuestas_por_defecto(self,sentence):
        for word in sentence.split():
            if word.lower() in self._textos["SALUDOS_INPUT"]:
                return random.choice(self._textos["SALUDOS_OUTPUT"])
            if word.lower() in self._textos["CHISTES_INPUT"]:
                return random.choice(self._textos["CHISTES_OUTPUT"])
            if word.lower() in self._textos["PRODUCTOS_INPUT"]:
                return "".join([x+".\n" for x in self._textos["PRODUCTOS_OUTPUT"]])
            

    def bucle_principal(self):
        if not self._status_bot['estado']:
            print(self._textos["ERROR_CONF"])
            return ""
        print(self._textos["BIENVENIDA"])
        paciencia=random.randint(5,20)
        while True:
            if paciencia==0:
                print(random.choice(self._textos["PACIENCIA_OUTPUT"]+"\n"))
                paciencia=random.randint(5,20)
            user_response = input().lower()
            if(user_response not in self._textos["DESPEDIDA_INPUT"]):
                if(user_response in self._textos["GRACIAS_INPUT"]): #Se podría haber definido otra función de coincidencia manual
                    print(random.choice(self._textos["GRACIAS_OUTPUT"]))
                else:
                    if(self.respuestas_por_defecto(user_response)!=None):
                        print("MUU-BOT: "+self.respuestas_por_defecto(user_response))
                    else: #Si la palabra insertada no es un saludo --> CORPUS
                        print("MUU-BOT: ",end="") 
                        print(self.response(user_response))
                        self._sent_tokens.remove(user_response) # para eliminar del corpus la respuesta del usuario y volver a evaluar con el CORPUS limpio
            else:
                print(random.choice(self._textos["DESPEDIDA_OUTPUT"]))
                return ""
            paciencia-=1