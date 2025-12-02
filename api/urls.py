from django.urls import path
from . import views

urlpatterns = [
    path('health', views.health, name='health'),
    path('retiros', views.crear_retiro, name='crear_retiro'),
    path('sql-test', views.sql_test, name='sql_test'),
]