"""Ce Module contien toutes  fonctions les permettants de
gerer permettant de gerer la page web"""

from itertools import chain
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import UserRegisterForm, FormReview, FormTicket
from .models import Review, Ticket, UserFollows


# Create your views here.

@login_required
def index(request):
    """Cette fonction permet de lister tous les tickets et critiques de
    l'utilisateur connecté et de ses abonnés"""

    context = {}
    if request.user.is_authenticated:
        # get followers of connected user
        followers = UserFollows.objects.filter(user=request.user.id)
        followed_user_ids = [follower.followed_user.id for follower in followers]
        tickets = Ticket.objects.filter(user=request.user.id) | Ticket.objects.filter(
            user__in=followed_user_ids)
        reviews = Review.objects.filter(ticket__in=[ticket for ticket in tickets])

        context['posts'] = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )

    return render(request, 'review/index.html', context)


def register(request):
    """Cette fonction permet à un utilisateur de créer un créer un compte
    afin de pourvoir se connecter sur le site"""

    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()  # register new user in the database
            username = form.cleaned_data.get('username')
            message = "Bienvenu {} ! Votre compte a été créé avec succès !".format(username)
            messages.success(request, message)
            return redirect('index')
    else:
        form = UserRegisterForm()

    context = {'form': form}
    return render(request, 'review/register.html', context)


@login_required
def create_ticket(request):
    """Cette fonction permet à l'utilisateur de créer un ticket."""

    if request.method == 'POST':
        form = FormTicket(request.POST, request.FILES)
        if form.is_valid():
            title = form.cleaned_data['title']
            description = form.cleaned_data['description']
            image = form.cleaned_data['image']
            # Registration of ticket in the database
            Ticket.objects.create(title=title, description=description,
                                  image=image, user=request.user)
            messages.success(request, "Votre ticket a été bien enregistré !")
            return redirect('index')
    else:
        form = FormTicket()

    context = {'form': form}
    return render(request, 'review/ticket.html', context)


@login_required
def ticket_update(request, ticket_id):
    """Cette fonction permet à l'utilisateur de modifier un ticket."""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == 'POST':
        form = FormTicket(request.POST, request.FILES, instance=ticket)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre ticket a bien été modifié!")
            return redirect('posts')
    else:
        form = FormTicket(instance=ticket)

    context = {'form': form, 'ticket_id': ticket_id}
    return render(request, 'review/ticket_update.html', context)


@login_required
def ticket_delete(request, ticket_id):
    """Cette fonction permet à l'utilisateur de supprimer un ticket"""

    ticket = get_object_or_404(Ticket, id=ticket_id)
    if request.method == "POST":
        ticket.delete()
        messages.success(request, "Votre ticket a bien été supprimé!")
        return redirect('posts')

    context = {'ticket': ticket}
    return render(request, 'review/posts.html', context)


@login_required
def create_review(request):
    """Cette fonction permet à l'utilisateur de créer un ticket et une critique
    en même temps."""

    if request.method == 'POST':
        form_ticket = FormTicket(request.POST, request.FILES, prefix="formTicket")
        form_review = FormReview(request.POST, request.FILES, prefix="formReview")
        if form_review.is_valid() and form_ticket.is_valid():
            review = form_review.save(commit=False)
            # --------------------Ticket creating --------------------
            # Registration of ticket in the database
            ticket = form_ticket.save(commit=False)
            ticket.user = request.user
            ticket.save()
            # --------------------Review creating --------------------
            review.ticket = ticket
            review.user = request.user
            review.save()
            messages.success(request, "Votre critique a été bien enregistré !")
            return redirect('index')
    else:
        form_ticket = FormTicket(prefix="formTicket")
        form_review = FormReview(prefix="formReview")

    context = {'form_review': form_review, 'form_ticket': form_ticket}
    return render(request, 'review/review.html', context)


@login_required
def review_update(request, review_id):
    """Cette fonction permet à l'utilisateur de modifier une critique."""

    review = get_object_or_404(Review, id=review_id)
    if request.method == 'POST':
        form = FormReview(request.POST, instance=review)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre critique a bien été modifié!")
            return redirect('posts')
    else:
        form = FormReview(instance=review)

    context = {'review': review, 'ticket': review.ticket, 'form': form}
    return render(request, 'review/reviewTicket_update.html', context)


@login_required
def review_delete(request, review_id):
    """Cette fonction permet à l'utilisateur de supprimer une critique."""

    review = get_object_or_404(Review, id=review_id)
    if request.method == "POST":
        review.delete()
        messages.error(request, "Votre critique a été bien supprimé!")
        return redirect('posts')

    context = {'review': review}
    return render(request, 'review/posts.html', context)


@login_required
def create_review_to_ticket(request, ticket_id):
    """Cette fonction permet à l'utilisateur de créer une critique
    à un ticket."""

    context = {}
    ticket = get_object_or_404(Ticket, pk=ticket_id)
    if request.method == 'POST':
        form = FormReview(request.POST)
        if form.is_valid():
            headline = form.cleaned_data['headline']
            body = form.cleaned_data['body']
            rating = form.cleaned_data['rating']
            # Registration of review in the database
            Review.objects.create(user=request.user, ticket=ticket,
                                  headline=headline, rating=rating, body=body)
            messages.success(request, "Votre critique a été bien enregistré !")
            return redirect('index')
    else:
        form = FormReview()
        context['ticket'] = ticket

    context['form'] = form
    return render(request, 'review/reviewTicket.html', context)


@login_required
def posts(request):
    """Cette fonction permet de lister tous les tickets et critiques de
    l'utilisateur connecté."""

    context = {}
    if request.user.is_authenticated:
        user_id = request.user.id
        tickets = Ticket.objects.filter(user=user_id).order_by('-time_created')
        reviews = Review.objects.filter(user=user_id).order_by('-time_created')
        context['tickets'] = tickets
        context['reviews'] = reviews

        # combine and sort the two types of posts
        context['posts'] = sorted(
            chain(reviews, tickets),
            key=lambda post: post.time_created,
            reverse=True
        )

    return render(request, 'review/posts.html', context)


@login_required
def abonnements(request):
    """Cette fonction permet de lister tous les abonnés d'un utilisateur"""

    followers = UserFollows.objects.filter(user=request.user.id)
    context = {'followers': followers}

    if request.method == 'POST':
        user_searched = request.POST.get('search')
        users = User.objects.filter(username__icontains=user_searched)
        # get all username of users followed
        users_followed = [follower.followed_user.username for follower in followers]
        # then exclude all followers and user authenticated
        users = users.exclude(username__in=users_followed).exclude(username=request.user.username)
        context['users'] = users
        context['user_searched'] = user_searched
        if not users.exists():
            context['infos'] = "Aucun utilisateur correspondant à:\
            {} n'a été trouvé".format(user_searched)

    return render(request, 'review/abonnement.html', context)


@login_required
def subscribe(request, to_follow_id):
    """Cette fonction permet de s'abonner à un utilisateur spécifique."""

    user_to_follow = get_object_or_404(User, id=to_follow_id)

    if request.method == 'POST':
        UserFollows.objects.create(user=request.user, followed_user=user_to_follow)
        messages.success(request, "Vous êtes maintenant abonné à un nouvel utilisateur")
        return redirect('abonnements')

    context = {'user_to_follow': user_to_follow}
    return render(request, 'review/abonnement.html', context)


@login_required
def unsubscribe(request, to_unfollow_id):
    """Cette fonction permet de se desabonner d'un auquel il est dejà abonné."""

    user_to_unfollow = get_object_or_404(User, id=to_unfollow_id)

    if request.method == 'POST':
        old_follower = UserFollows.objects.filter(user=request.user, followed_user=user_to_unfollow)
        old_follower.delete()
        messages.success(request, "Vous n'êtes plus abonné à un à un de vos utilisateurs")
        return redirect('abonnements')

    context = {'user_to_unfollow': user_to_unfollow}
    return render(request, 'review/abonnement.html', context)
