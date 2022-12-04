import re

from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View

from my_library import constant


class Login(View):
  def get(self, request):
    """
    登录页面
    """
    return render(request, 'login.html', {})

  def post(self, request):
    """
    登录
    """
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = auth.authenticate(request, username=username, password=password)
    if user is not None and user.is_active:
      auth.login(request, user)
      # 如果是手机号登录，重定向到读者首页
      if re.match(constant.REGEX.phone_number, username):
        return redirect('app:index')
      # 否则重定向到管理后台
      else:
        return redirect('admin:index')
    else:
      return render(request, 'login.html', {'msg': '用户名或密码错误！'})


@method_decorator(login_required, name='dispatch')
class Index(View):
  def get(self, request):
    """
    读者首页
    """
    return render(request, 'index.html', {})
