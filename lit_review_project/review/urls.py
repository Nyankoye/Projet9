from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('review/', views.createReview, name='review'),
    path('ticket/', views.createTicket, name='ticket'),
    path('review/<int:ticket_id>', views.createReviewToTicket, name='reviewTicket'),
]