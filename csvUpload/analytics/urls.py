from . import views
from django.urls import path

urlpatterns = [

    path('', views.home, name='home'),
    path('results', views.results, name='results'),
    path('results1', views.results1, name='results1'),
]