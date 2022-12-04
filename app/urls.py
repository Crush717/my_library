from django.contrib.auth.decorators import login_required
from django.urls import path

from app import views

# 命名空间
app_name = 'app'
# 访问地址
urlpatterns = [
  path('login/', views.Login.as_view(), name='login'),
  # 装饰基于类的视图：https://docs.djangoproject.com/zh-hans/4.1/topics/class-based-views/intro/#decorating-class-based-views
  path('', login_required(views.Index.as_view()), name='index'),
]
