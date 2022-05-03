
from django.urls import path
from myapp import views
urlpatterns = [
    path('', views.index), # 사용자가 home으로 들어왔을 때 ''으로 나타냄. + views 모듈을 import해서 index 함수 사용
    path('create/',views.create),  # create/ 경로로 들어왔을 때
    path('read/<id>/', views.read), # <>는 가변변수에대한 처리
    path('update/<id>/', views.update),
    path('delete/', views.delete)
]
