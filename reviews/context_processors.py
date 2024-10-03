# reviews/context_processors.py
from .models import Category
from deals.models import DealsCategory

def category_links(request):
    categories = Category.objects.all()
    return {'categories': categories}

def deals_categories(request):
    return {
        'deals_categories': DealsCategory.objects.all()
    }
