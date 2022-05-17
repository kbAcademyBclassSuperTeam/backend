from django.urls import path
from . import views

urlpatterns = [
    path('', views.main , name='main'),
    path('search/', views.search_table, name="search_table"),
    path('blob/', views.blob_table, name="blob_table"),
    

]