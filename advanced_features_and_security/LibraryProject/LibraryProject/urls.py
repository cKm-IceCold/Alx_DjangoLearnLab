from django.urls import path
from django.contrib import admin

urlpatterns = [
   path('admin/', admin.site.urls),
    path('', include('relationship_app.urls'))
    path('home/', views.homepage, name='home' ),
    path('home/', views.homepage, name='home' ),
    path("newsite/",views.hiddenpage, name='hiddenpage'),
    path('review/', views.BookReviewView.as_view(), name='bookreview'),
    path('booklist/', views.booklist, name='booklist'),
    path("accounts/login/",views.LoginView.as_view(), name='login'),
    path("accounts/logout/", views.LogoutView.as_view(), name='logout'),
    path('accounts/register/', views.RegisterView.as_view(), name='register'),
    path('accounts/profile/', views.ProfileView.as_view(), name='profile'),
]