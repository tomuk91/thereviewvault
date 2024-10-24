from django.shortcuts import render, get_object_or_404

# Create your views here.
from .models import Deal, DealsCategory

def deals_list(request):
    deals = Deal.objects.all()
    return render(request, 'deals/deals_list.html', {'deals': deals})

def deals_by_category(request, slug):
    category = get_object_or_404(DealsCategory, slug=slug)
    deals = Deal.objects.filter(category=category)

    # Meta title, description, and keywords
    title = f"{category.name} Deals - The Vault Reviews"
    meta_description = f"Explore the best deals in {category.name}. Find discounted products and exclusive offers in the {category.name} category."
    meta_keywords = f"{category.name} deals, best {category.name} discounts, {category.name} offers, product deals, discounted {category.name} products"

    return render(request, 'deals/deals_by_category.html', {
        'category': category,
        'deals': deals,
        'title': title,
        'meta_description': meta_description,
        'meta_keywords': meta_keywords,
    })


