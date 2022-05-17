from django.urls import path
from . import views

urlpatterns = [
    path('', views.post , name='post'),
    path('search/', views.search_table, name="search_table"),
    path('blob/', views.blob_table, name="blob_table"),
    path('createSound', views.createSound, name="create_sound"),
    

]