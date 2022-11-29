from django.urls import path

from main import views

# 命名空间
app_name = 'main'
# 访问地址
urlpatterns = [
    # 登录页面
    path('login', views.loginView, name='loginView'),

    # 登录
    path('api/login', views.loginApi, name='loginApi')
]
