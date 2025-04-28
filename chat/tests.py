from dbctrl import Bot_db
from django.test import TestCase
from bot import botest

# Create your tests here.
'''
bot=botest()
print(f"{bot}...\n")
print(bot.bucle_principal())'''

if __name__=='__main__':
    with Bot_db() as db:
        resultado=db.get_productos()
    
    for x in resultado['data']: print(x)
        