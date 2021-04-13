from django import forms
from django.forms import ModelForm, ImageField, NumberInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Ticket


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FormReview(ModelForm):
    class Meta:
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating': NumberInput(attrs={'maxlength': '5'}),
        }

class FormTicket(ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'image']