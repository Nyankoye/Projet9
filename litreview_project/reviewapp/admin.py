from django.contrib import admin
from .models import Ticket, Review, UserFollows

# Register your models here.

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    pass

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    pass

@admin.register(UserFollows)
class UserFollowsAdmin(admin.ModelAdmin):
    pass