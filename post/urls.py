from django.urls import path
from . import views

urlpatterns = [
    path('', views.post , name='post'),
    path('search/', views.search_table, name="search_table"),
    path('blob/', views.blob_table, name="blob_table"),
    path('save_audio/', views.save_audio, name="save_audio"),

]