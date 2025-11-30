from django.urls import path
from .import views 

#Url Configuration
urlpatterns = [
# the path function return a url pattern object.  In the argument it can be a rout or url
  path('hello/', views.say_hello)
]
