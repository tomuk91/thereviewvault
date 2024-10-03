from django.urls import path
from . import views

urlpatterns = [
    path('', views.deals_list, name='deals_list'),
    path('category/<slug:slug>/', views.deals_by_category, name='deals_category'),
]
