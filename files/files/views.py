from django.shortcuts import render
from django.views.generic import TemplateView, ListView, CreateView
from django.core.files.storage import FileSystemStorage
from django.shortcuts import redirect
from .forms import BookForm
from .models import Book
from django.urls import reverse_lazy
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.http import HttpResponseRedirect
from .forms import BookForm


class Home(TemplateView):
    template_name = 'home.html'


@login_required()
def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'upload.html', context)


@login_required()
def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {
        'books': books
    })



def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')


@login_required()
def upload_book(request):
    if not (request.user.is_staff or request.user.is_superuser):
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()

    return render(request, 'upload_book.html', {
        'form': form
    })


class BookListView(ListView):
    model = Book
    template_name = 'class_book_list.html'
    context_object_name = 'books'



class UploadBookView(CreateView):
    model = Book
    form_class = BookForm
    #fields = ('title', 'author', 'pdf', 'cover')
    success_url = reverse_lazy ('class_book_list')
    template_name = 'upload_book.html'


def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:    
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {
        'form': form
    })
