from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Deal, DealsCategory

def deals_list(request):
    deals = Deal.objects.all()
    return render(request, 'deals/deals_list.html', {'deals': deals})

def deals_by_category(request, slug):
    category = get_object_or_404(DealsCategory, slug=slug)
    deals = Deal.objects.filter(category=category)
    return render(request, 'deals/deals_by_category.html', {'category': category, 'deals': deals})
