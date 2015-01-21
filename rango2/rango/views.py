from django.shortcuts import render

from django.http import HttpResponse

def index(request):

    context_dict = { 'boldmessage': "I am bold font"}

    return render( request, 'rango/index.html', context_dict)

def about(request):

    context_dict = { 'boldmessage': "About page. Put together by Lovisa Sundin, 2092502s" }

    return render( request, 'rango/about.html', context_dict)
    
    #return HttpResponse("About page. This tutorial has been put together by Lovisa Sundin, 2092502s. <br/> <a href='/rango/'>Index</a>")


