from django import template
from news.models import NewsArticle

register = template.Library()

@register.inclusion_tag('news/latest_news_sidebar.html')
def latest_news(count=5):
    latest_articles = NewsArticle.objects.all()[:count]
    return {'latest_articles': latest_articles}
