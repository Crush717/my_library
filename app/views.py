from django.shortcuts import render
from django.template.context_processors import request
from django.views import generic, View

from app.models import Reader


class Login(View):
  def get(self, request):
    """
    登录页面
    """
    return render(request, 'login.html', {})
