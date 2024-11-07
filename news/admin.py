from django.contrib import admin
from .models import NewsArticle, NewsCategory

@admin.register(NewsArticle)
class NewsArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_date')
    prepopulated_fields = {'slug': ('title',)}  # Auto-generate the slug from the title

admin.site.register(NewsCategory)