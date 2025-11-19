from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly 

# Create your views here.
#class BookList(ListAPIView):
#queryset = Book.objects.all()
# serializer_class = BookSerializer

#ViewSets
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

 #Implementing permissions in view.py
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

class SecureBookViewSet(viewsets.ModelViewSet):
   queryset = Book.objects.all()
   serializer_class = BookSerializer

   permission_classes = [IsAuthenticated, IsAdminUser]

class PublicReadOnlyBookViewSet(viewsets.ModelViewSet):
   queryset = Book.objects.all()
   serializer_class = BookSerializer
   


