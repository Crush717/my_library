from django.shortcuts import render
from django.template.context_processors import request
from django.views import generic

from main.models import Reader


def loginView(request):
    """
    登录页面
    """
    return render(request, 'main/login.html', {})


def loginApi(request, phone_number, password):
    """
    登录
    """
    # 根据手机号获取读者
    reader = Reader.objects.filter(phone_number=phone_number)\
    # 密码

    # 跳转到首页



