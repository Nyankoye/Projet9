"""Ce Module contien toutes classe et methodes les permettants de gerer
l'affichage de la page de l'administrateur"""

from django.contrib import admin
from .models import Review, Ticket, UserFollows


# Register your models here.

class ReviewInline(admin.TabularInline):
    """cette classe permet d'afficher les critiques d'un ticket."""

    model = Review
    fieldsets = [
        (None, {'fields': ['headline', 'body', 'user', 'rating']})
    ]  # list columns
    extra = 0
    readonly_fields = ['time_created']
    verbose_name = "Critique"
    verbose_name_plural = "Critiques"


@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    """Classe des administratrice des Tickets."""

    readonly_fields = ['time_created']
    search_fields = ['title']
    inlines = [ReviewInline, ]
    list_filter = ['time_created', 'user']


@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    """Classe des administratrice des Critiques."""

    readonly_fields = ['time_created']
    search_fields = ['headline']
    list_filter = ['time_created', 'user']


@admin.register(UserFollows)
class AdminUserFollows(admin.ModelAdmin):
    """Classe des administratrice des abonnements."""

    def has_add_permission(self, request):
        """Cette fonction empêche l'admin d'ajouter des abonnés à un utilisateur"""
        return False
