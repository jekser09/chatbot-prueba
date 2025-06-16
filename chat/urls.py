from django.urls import path
from . import views

urlpatterns=[
    path("mubot/",views.chat,name="mubot"),
    path('conversacion/<str:texto>',views.conversacion,name='conversacion'),
    path('estadistica/',views.estadisticas,name='estadisticas')
]