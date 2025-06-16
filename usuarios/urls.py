from . import views
from django.urls import path

urlpatterns = [
    path("",views.login,name="index"),
    path("probar_db/",views.probar_db,name="probar_db"),
    path("logout/",views.logout,name="logout"),
    path("menu_general/",views.menu_general,name="menu_general")
]