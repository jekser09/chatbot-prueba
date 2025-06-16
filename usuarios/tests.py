from django.test import TestCase
from dbctrl import sql_usuarios
from django.core.management.utils import get_random_secret_key
# Create your tests here.
with sql_usuarios() as db:
    print(db.login(usuario="ANALISTA",clave="AV1379"))
