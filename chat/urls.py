from django.urls import path
from . import views

urlpatterns=[
    path("",views.chat,name="chatbot"),
    path('conversacion/<str:texto>',views.conversacion,name='conversacion'),
    path('estadistica/',views.estadisticas,name='estadisticas')
]