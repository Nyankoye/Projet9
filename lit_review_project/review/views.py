from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm

# Create your views here.

@login_required
def index(request):
    return render(request, 'review/index.html')

def register(request):

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save() # register new user in the database
            username = form.cleaned_data.get('username')
            message = "Bienvenu {} ! Votre compte a été créé avec succès !".format(username)
            messages.success(request, message)
            return redirect('index')
    else:
        form = UserRegisterForm()
    
    context = {'form':form}
    return render(request, 'review/register.html', context)