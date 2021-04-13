from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
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

    context = {
        'tickets':tickets
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

@login_required
def createTicket(request):
    if request.method == 'POST':
        form = FormTicket(request.POST, request.FILES)
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
        form = FormTicket()

    context = {'form':form}
    return render(request, 'review/ticket.html', context)

@login_required
def ticket_update(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = FormTicket(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre ticket a bien été modifié!")
            return redirect('posts')
    else:
        form = FormTicket(instance=ticket)

    context = {'form':form,'ticket_id':ticket_id}
    return render(request, 'review/ticket_update.html', context)

@login_required
def ticket_delete(request,ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Votre ticket a bien été supprimé!")
        return redirect('posts')

    context = {'ticket':ticket}
    return render(request, 'review/posts.html', context)

@login_required
def createReview(request):
    if request.method == 'POST':
        formTicket = FormTicket(request.POST, request.FILES, prefix="formTicket")
        formReview = FormReview(request.POST, request.FILES,prefix="formReview")
        if formReview.is_valid() and formTicket.is_valid():
           
            review = formReview.save(commit=False)
            #--------------------Ticket creating --------------------  
            # Registration of ticket in the database
            ticket = formTicket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            #--------------------Review creating --------------------
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Votre critique a été bien enregistré !")
            return redirect('index')
    else:
        formTicket = FormTicket(prefix="formTicket")
        formReview = FormReview(prefix="formReview")

    context = {'formReview':formReview, 'formTicket':formTicket}
    return render(request, 'review/review.html', context)

def review_update(request,review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = FormReview(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre critique a bien été modifié!")
            return redirect('posts')
    else:
        form = FormReview(instance=review)

    context = {'review':review, 'ticket':review.ticket, 'form':form}
    return render(request, 'review/reviewTicket_update.html', context)

def review_delete(request, review_id):
    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        review.delete()
        messages.error(request, "Votre critique a été bien supprimé!")
        return redirect('posts')

    context = {'review':review}
    return render(request, 'review/posts.html', context)

@login_required
def createReviewToTicket(request, ticket_id):
    context = {}
    ticket = get_object_or_404(Ticket,pk = ticket_id)
    if request.method == 'POST':
        form = FormReview(request.POST)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            body = form.cleaned_data['body']
            rating = form.cleaned_data['rating']
            # Registration of review in the database
            review = Review.objects.create(user=request.user,ticket=ticket,
                                            headline=headline,rating=rating,body=body)
            messages.success(request, "Votre critique a été bien enregistré !")
            return redirect('index')
    else:
        form = FormReview()
        context['ticket'] = ticket

    context['form'] = form
    return render(request, 'review/reviewTicket.html', context)


def posts(request):
    if request.user.is_authenticated:
        user_id = request.user.id
        tickets = Ticket.objects.filter(user = user_id).order_by('-time_created')
        reviews = Review.objects.filter(user=user_id).order_by('-time_created')
        
    context = {
        'tickets':tickets,
        'user_id':user_id,
        'reviews':reviews
    }
    return render(request, 'review/posts.html', context)

def abonnements(request):
    followers = UserFollows.objects.filter(user=request.user.id)
    context ={'followers':followers}

    if request.method == 'POST': 
        user_searched = request.POST.get('search')
        users = User.objects.filter(username__icontains=user_searched)
        context['users'] = users
        context['user_searched'] = user_searched
        if not users.exists():
            context['message'] = "Aucun utilisateur n'a été trouvé pour:\
            {}".format(user_searched)

    return render(request, 'review/abonnement.html', context)


