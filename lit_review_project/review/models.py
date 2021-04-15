"""Ce module contient les classes et les methodes qui permettent de
créer la basse de données grâces à l'ORM de django"""

from django.core.validators import MinValueValidator, MaxValueValidator
from django.conf import settings
from django.db import models


# Create your models here.

class Ticket(models.Model):
    """Cette classe permet de creer une table Ticket avec les champs ci-dessous
    grâce à l'ORM de django"""

    # Your Ticket model definition goes here
    title = models.CharField('Titre', max_length=128)
    description = models.TextField('Description', max_length=2048, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField('Image', null=True, blank=True, upload_to='img')
    time_created = models.DateTimeField('Date', auto_now_add=True)

    def __str__(self):
        """Permet d'afficher le titre de l'objet Ticket à la place de l'objet"""
        return self.title


class Review(models.Model):
    """Cette classe permet de creer une table Review avec les champs ci-dessous
    grâce à l'ORM de django"""

    ticket = models.ForeignKey(to=Ticket, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(
        # validates that rating must be between 0 and 5
        'note', validators=[MinValueValidator(0), MaxValueValidator(5)])
    headline = models.CharField('Titre', max_length=128)
    body = models.TextField('Commentaire', max_length=8192, blank=True)
    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    time_created = models.DateTimeField('Date', auto_now_add=True)

    def __str__(self):
        """Cette methode permet d'afficher le titre de l'objet Review à la place de l'objet"""
        return self.headline

    class Meta:
        """Cette classe permet permet de specifier certain comportement
        de la table Review."""
        verbose_name = "Critique"
        verbose_name_plural = "Critiques"


class UserFollows(models.Model):
    # Your UserFollows model definition goes here

    user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='following')

    followed_user = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='followed_by')

    def __str__(self):
        """Cette methode permet d'afficher l'utilisateur de l'objet UserFollows
        à la place de l'objet"""
        return self.user

    class Meta:
        """Cette classe permet permet de specifier certain comportement
        de la table UserFollows"""
        # ensures we don't get multiple UserFollows instances
        # for unique user-user_followed pairs
        unique_together = ('user', 'followed_user',)
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"
