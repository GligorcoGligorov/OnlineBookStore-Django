import datetime
from datetime import date
from django.shortcuts import render,get_object_or_404,redirect
from .models import Book,Card,Author
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from .forms import BookForm




@unauthenticated_user
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user_type = request.POST.get('user_type')
            if user_type == 'customer':
                user.is_superuser = False
                user.is_staff = False
            elif user_type == 'seller':
                user.is_superuser = True
                user.is_staff = True
            user.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


@unauthenticated_user
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('index')
        else:
            # Handle invalid login credentials here, such as displaying an error message
            pass
    return render(request, 'login.html')



@unauthenticated_user
def registerAndLogin(request):
    return render(request,'registerAndLogin.html')


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('registerAndLogin')
    return render(request, 'logout.html')


def get_user_cart(user):
    if user.is_authenticated:
        card_num = user.id
        card_expiration_date = date.today().isoformat()
        cart, created = Card.objects.get_or_create(
            card_num=card_num,
            card_expiration_date=card_expiration_date
        )

        # Check if multiple cards exist for the user and delete the extras
        cards = Card.objects.filter(card_num=card_num)
        if cards.count() > 1:
            cards.exclude(pk=cart.pk).delete()

        return cart
    return None

@login_required(login_url='login_view')
def index(request,bookss=None):
    search_query = request.GET.get('search')

    if search_query:
        books = Book.objects.filter(title__icontains=search_query) | Book.objects.filter(
            author__name__icontains=search_query)
    elif bookss:
        books = bookss
    else:
        books = Book.objects.all()

    cart = get_user_cart(request.user)
    numBooks = cart.books.count() if cart else 0
    context={"books" : books, 'numBooks': numBooks}
    return render(request, 'index.html',context=context)


@login_required(login_url='login_view')
def showBook(request, id):

    book = get_object_or_404(Book, id=id)
    cart = get_user_cart(request.user)
    numBooks = cart.books.count() if cart else 0
    context = {"book": book, 'numBooks':numBooks}
    return render(request, 'showBook.html', context=context)


@login_required(login_url='login_view')
def addToCart(request):
    if request.method == 'POST':
        book_id = request.POST.get('book_id')
        book = get_object_or_404(Book, id=book_id)

        cart, created = Card.objects.get_or_create(card_num=request.user.id)

        cart.books.add(book)

        cart.save()

        return redirect('showBook', id=book_id)

    return redirect('index')

@login_required(login_url='login_view')
def cartBooks(request):
    cart = get_object_or_404(Card, card_num=request.user.id)
    books = cart.books.all()
    total = 0.0
    for book in books:
        total += book.price

    context = {
        'books': books,
        'total': total
    }

    return render(request, 'card.html', context=context)

@login_required(login_url='login_view')
def successBuy(request):
    cart = get_user_cart(request.user)
    context = {}
    total = 0.0
    if cart:
        if cart.books.exists():
            cart.books.clear()
            cart.save()
        else:
            context = {'cart_empty':True, 'total':total}
            return render(request, 'card.html',context=context)


    return render(request, 'successBuy.html',context=context)


@login_required(login_url='login_view')
def addBook(request):
    authors = Author.objects.all()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.save()
            return redirect('index')
    else:
        form = BookForm()

    context = {'form': form, 'authors': authors}
    return render(request, 'addBook.html', context=context)


@login_required(login_url='login_view')
def editBook(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('index')
    else:
        form = BookForm(instance=book)

    context = {'form': form, 'book':book}
    return render(request, 'editBook.html', context=context)


@login_required(login_url='login_view')
def deleteBook(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
        return redirect('index')

    context = {'book': book}
    return render(request, 'deleteBook.html', context=context)

