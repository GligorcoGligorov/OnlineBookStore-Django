"""
URL configuration for bookStoreProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from bookstore.views import index,showBook,addToCart,cartBooks,successBuy, registerAndLogin, register, login_view, logout_view, addBook, deleteBook, editBook
urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', index, name='index'),
    path('index/<str:bookss>/', index, name='index_with_books'),
    path('showBook/<int:id>/', showBook, name='showBook'),
    path('addToCart/', addToCart, name='addToCart'),
    path('cartBooks/', cartBooks, name='cartBooks'),
    path('successBuy/', successBuy, name='successBuy'),
    path('registerAndLogin/', registerAndLogin, name='registerAndLogin'),
    path('register/', register, name='register'),
    path('login_view/', login_view, name='login_view'),
    path('logout/', logout_view, name='logout'),
    path('addBook/', addBook, name='addBook'),
    path('editBook/<int:id>/', editBook, name='editBook'),
    path('deleteBook/<int:id>/', deleteBook, name='deleteBook'),

]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
