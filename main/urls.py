from django.urls import path
from . import views

app_name = "NEOWS"

urlpatterns = [
	path('', views.index, name="home"),
	path('results', views.results, name="results"),

]