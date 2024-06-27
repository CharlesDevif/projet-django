import django_filters
from .models import Article

class ArticleFilter(django_filters.FilterSet):
    class Meta:
        model = Article
        fields = {
            'title': ['icontains'],
            'category': ['exact'],
            'user': ['exact'],
        }
