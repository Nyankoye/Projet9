from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('review/', views.createReview, name='review'),
    path('review/<int:review_id>', views.review_update, name='review_update'),
    path('review/delete/<int:review_id>', views.review_delete, name='review_delete'),
    path('review/<int:ticket_id>/', views.createReviewToTicket, name='reviewTicket'),
    path('ticket/', views.createTicket, name='ticket'),
    path('ticket/<int:ticket_id>/', views.ticket_update, name='ticket_update'),
    path('ticket/delete/<int:ticket_id>/', views.ticket_delete, name='ticket_delete'),
    path('posts/', views.posts, name='posts'),
    path('abonnements/', views.abonnements, name='abonnements'),
    
]