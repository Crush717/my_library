from django.urls import path

from app import views

# 命名空间
app_name = 'app'
# 访问地址
urlpatterns = [
  path('login/', views.Login.as_view(), name='login'),
  path('', views.Index.as_view(), name='index'),
]
