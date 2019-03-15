#！/usr/bin/env.python
# _*_ coding:utf-8 _*_

from django.shortcuts import render

def home(request):
    """
    Renders home template
    """
    return render(request, 'home.html')