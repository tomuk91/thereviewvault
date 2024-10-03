from django.contrib import admin
from .models import Category, Review
from deals.models import Deal, DealsCategory


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'rating', 'publication_date', 'product_code', 'review_of_the_week')
    list_editable = ('review_of_the_week',)
    search_fields = ('title', 'author', 'tags__name', 'product_code')
    prepopulated_fields = {'slug': ('title',)}
    list_filter = ('tags',)  # Filtering by tags


admin.site.register(Category)
admin.site.register(DealsCategory)

@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    list_display = ('title', 'price', 'created_at', 'coupon_code')  # Customize fields to display in the admin list view
    search_fields = ('title', 'description')         # Add a search bar to search deals
    list_filter = ('created_at',)                    # Filter by date
    ordering = ('-created_at',)                      # Order deals by most recent first