from django.contrib import admin
from .models import Review, Ticket, UserFollows 


# Register your models here.

@admin.register(Review)
class AdminReview(admin.ModelAdmin):
    pass

@admin.register(Ticket)
class AdminTicket(admin.ModelAdmin):
    pass

@admin.register(UserFollows)
class AdminUserFollows(admin.ModelAdmin):
    pass