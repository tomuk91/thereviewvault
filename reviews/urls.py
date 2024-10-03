from django.urls import path
from . import views
from .views import privacy_policy

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('review/<slug:slug>/', views.review_detail, name='review_detail'),
    path('category/<slug:slug>/', views.category_reviews, name='category_reviews'),
    path('search/', views.search_reviews, name='search_reviews'),
    path('tag/<slug:tag_slug>/', views.tagged_reviews, name='tagged_reviews'),
    path('reviews/rating/<str:rating>/', views.reviews_by_rating, name='reviews_by_rating'),
    path('privacy-policy/', privacy_policy, name='privacy_policy'),
    path('about/', views.about_us, name='about_us'),
    path('terms/', views.terms_conditions, name='terms_conditions'),
    path('contact/', views.contact_us, name='contact_us'),
    ]
