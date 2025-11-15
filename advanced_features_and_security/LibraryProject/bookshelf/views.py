from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import permission_required, login_required
from .models import Book, Review
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import BookReviewForm

# Create your views here.

def homepage(request):
    template = "bookshelf/home.html/"
    return render(request, template_name=template, context={})

@login_required
@permission_required('bookshelf.can_edit', raise_exception=True)
def hiddenpage(request):
    return HttpResponse("<h1>If you are here you can edit Books.</h1>")

# Views for listing and displaying Books
def booklist(request):
    """View to display list of all books."""
    books = Book.objects.all()
    context = {'books': books}
    return render(request, 'bookshelf/book_list.html', context=context)

class BookReviewView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Review
    form_class = BookReviewForm
    template_name = 'bookshelf/form_example.html'
    success_url = reverse_lazy('booklist')  
    permission_required = 'bookshelf.review_book'
    permission_denied_message = 'Sorry You do not have access to review a book'

    def form_valid(self, form):
        # Assign the currently logged-in user as the review author
        form.instance.user = self.request.user
        return super().form_valid(form)


#Recreated this to isolate the bookshelf app as it's standalone app.
# User registration and profile views
from django.views.generic import TemplateView
from typing import Any
from django.contrib.auth.views import LoginView, LogoutView
from LibraryProject import settings
from .forms import MyUserCreationForm

class RegisterView(CreateView):
    """View for user registration."""

    model = settings.AUTH_USER_MODEL
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'bookshelf/register.html'

class ProfileView(TemplateView):
    """User profile view."""
    template_name = 'bookshelf/profile.html'

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["user"] = self.request.user
        return context

class LoginView(LoginView):
    """User login view."""
    template_name = 'bookshelf/login.html'

class LogoutView(LogoutView):
    """User logout view."""
    template_name = 'bookshelf/logout.html'