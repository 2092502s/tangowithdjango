from django.shortcuts import render
#from rango.models import Category #CH7
from django.http import HttpResponse

def index(request):

    #category_list = Category.objects.order_by('-likes')[:5] #CH7
    context_dict = { 'boldmessage': "I am bold font"}
    #context_dict = {'categories': category_list} #CH7

    return render( request, 'rango/index.html', context_dict)

def about(request):

    context_dict = { 'boldmessage': "About page. Put together by Lovisa Sundin, 2092502s" }

    return render( request, 'rango/about.html', context_dict)
    
    #return HttpResponse("About page. This tutorial has been put together by Lovisa Sundin, 2092502s. <br/> <a href='/rango/'>Index</a>")


