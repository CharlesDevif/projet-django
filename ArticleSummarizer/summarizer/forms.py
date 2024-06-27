from django import forms
from .models import Article, Summary, Category

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content', 'category']

class SummaryForm(forms.ModelForm):
    class Meta:
        model = Summary
        fields = ['summary_text']

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name']
