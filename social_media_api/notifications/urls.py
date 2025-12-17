from django.urls import path
from .views import NotificationListView  # replace with your actual view

urlpatterns = [
    path('', NotificationListView.as_view(), name='notifications'),
]
