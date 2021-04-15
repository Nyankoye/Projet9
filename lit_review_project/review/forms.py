"""Ce module contient toutes les classes et methodes permettant de gerer
les formulaires de la page web"""

from django import forms
from django.forms import ModelForm, NumberInput
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Review, Ticket


class UserRegisterForm(UserCreationForm):
    """Classe permettant de créer le formulaire d'inscription"""
    email = forms.EmailField()

    class Meta:
        """Cette classe permet permet de specifier certain comportement
        du formulaire d'enregistrement."""
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class FormReview(ModelForm):
    """Classe permettant de créer le formulaire de creation de critique"""

    class Meta:
        """Cette classe permet permet de specifier certain comportement 
        du formulaire de critique."""
        model = Review
        fields = ['headline', 'rating', 'body']
        widgets = {
            'rating': NumberInput(attrs={'maxlength': '5'}),
        }


class FormTicket(ModelForm):
    """Classe permettant de créer le formulaire d'inscription"""

    class Meta:
        """Cette classe permet permet de specifier certain comportement 
        du formulaire de creation de ticket."""
        model = Ticket
        fields = ['title', 'description', 'image']
