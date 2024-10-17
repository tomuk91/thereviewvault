# reviews/context_processors.py
from .models import Category
from deals.models import DealsCategory
from django.conf import settings

def category_links(request):
    categories = Category.objects.all()
    return {'categories': categories}

def deals_categories(request):
    return {
        'deals_categories': DealsCategory.objects.all()
    }

def global_settings(request):
    return {
        'ENABLE_GOOGLE_ANALYTICS': settings.ENABLE_GOOGLE_ANALYTICS,
    }