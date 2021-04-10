from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm, FormReview, FormTicket
from .models import Review, Ticket, UserFollows

# Create your views here.

@login_required
def index(request):
    if request.user.is_authenticated:
        # get followers of connected user
        followers = UserFollows.objects.filter(user=request.user.id)
        followed_user_ids = [follower.followed_user.id for follower in followers]

        tickets = Ticket.objects.filter(user=request.user.id).order_by('-time_created')|\
        Ticket.objects.filter(user__in=followed_user_ids).order_by('-time_created')

        # get all rewviews of connected user and its followers
        reviews = Review.objects.filter(ticket__in=[ticket.id for ticket in tickets])

    context = {
        'reviews':reviews,
        'tickets':tickets,
        'follower_ids':followed_user_ids
    }

    return render(request, 'review/index.html', context)


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


def createTicket(request):
    if request.method == 'POST':
        form = FormTicket(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            # Registration of ticket in the database
            ticket = Ticket.objects.create(title=title,description=description,
                                            image=image,user=request.user)
            messages.success(request, "Votre ticket a été bien enregistré !")
            return redirect('index')
    else:
        form = FormTicket(instance=request.user)

    context = {'form':form}
    return render(request, 'review/ticket.html', context)

def createReview(request):
    if request.method == 'POST':
        formTicket = FormTicket(request.POST,request.FILES,instance=request.user)
        formReview = FormReview(request.POST,instance=request.user)
        if formReview.is_valid() and formTicket.is_valid():
            FormTicket.save()
            FormReview.save()
            messages.success(request, "Votre critique a été bien enregistré !")
            return redirect('index')
    else:
        formReview = FormReview(instance=request.user)
        formTicket = FormTicket(instance=request.user)

    context = {'formReview':formReview, 'formTicket':formTicket}
    return render(request, 'review/review.html', context)

def createReviewToTicket(request, ticket_id):
    context = {}
    if request.method == 'POST':
        form = FormReview(request.POST, instance=request.user)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            body = form.cleaned_data['body']
            rating = form.cleaned_data['rating']
            # Registration of review in the database
            review = Review.objects.create(user=request.user.id,ticket=book_id,
                                            headline=headline,rating=rating,body=body)
            messages.success(request, "Votre ticket a été bien enregistré !")
            return redirect('index')
    else:
        form = FormReview(instance=request.user)
        ticket = get_object_or_404(Ticket,pk = ticket_id)
        context['ticket'] = ticket

    context[form] = form
    return render(request, 'review/reviewTicket.html', context)

