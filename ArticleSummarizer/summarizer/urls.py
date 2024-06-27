from django.urls import path
from . import views
from .views import ArticleFilterView


urlpatterns = [
    path('', views.index, name='index'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('articles/', ArticleFilterView.as_view(), name='article_list'),

    path('article/add/', views.add_article, name='add_article'),
    path('article/<int:pk>/generate_summary/', views.generate_summary, name='generate_summary'),

    path('article/<int:article_pk>/delete_summary/<int:summary_pk>/', views.delete_summary, name='delete_summary'),
    path('article/<int:pk>/delete/', views.delete_article, name='delete_article'),
]
