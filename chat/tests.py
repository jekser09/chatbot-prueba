from django.test import TestCase
from bot import botest

# Create your tests here.
bot=botest()
print(f"{bot}...\n")
bot.bucle_principal()
