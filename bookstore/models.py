from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=100)
    surname = models.CharField(max_length=100)
    year_of_birth = models.IntegerField()
    country = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} {self.surname}"

class Book(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    genre = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    photo = models.ImageField(upload_to='book_photos', null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return self.title

class Card(models.Model):
    total = models.FloatField(default=0.0, null=True, blank=True)
    card_num = models.IntegerField()
    card_holder_name = models.CharField(max_length=100)
    card_expiration_date = models.DateField()
    cvc = models.IntegerField(default=0)
    books = models.ManyToManyField(Book)

    def __str__(self):
        return f"Card: {self.card_num}"