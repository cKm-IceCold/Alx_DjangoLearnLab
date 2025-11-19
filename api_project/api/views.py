from django.shortcuts import render
from .models import Book
from .serializers import BookSerializer
from rest_framework.generics import ListAPIView
from rest_framework import viewsets
 

# Create your views here.
#class BookList(ListAPIView):
#queryset = Book.objects.all()
# serializer_class = BookSerializer

#ViewSets
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


