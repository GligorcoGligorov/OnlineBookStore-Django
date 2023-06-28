from django import forms
from .models import Book
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class BookForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            print(field)
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = Book
        fields = ['title', 'author', 'genre', 'description', 'price', 'photo']



User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=[('customer', 'Customer'), ('seller', 'Seller')])

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('user_type',)