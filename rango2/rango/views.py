from django.shortcuts import render

from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello world! <br/> <a href='/rango/about'>About</a>")

def about(request):
    return HttpResponse("About page. This tutorial has been put together by Lovisa Sundin, 2092502s. <br/> <a href='/rango/'>Index</a>")


