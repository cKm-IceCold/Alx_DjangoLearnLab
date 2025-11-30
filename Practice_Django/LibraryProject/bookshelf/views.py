from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def say_hello(request):

#return HttpResponse("Hello World") 

#To return a template with html content
 return render(request, 'hello.html')
