from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Article, Summary, Category
from .forms import ArticleForm, SummaryForm, CategoryForm
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.output_parsers import PydanticOutputParser
from .config import OPENAI_API_KEY
from .pydantic_models import SummaryModel
from django_filters.views import FilterView
from .filters import ArticleFilter
from django.contrib.auth.models import User
import logging



class ArticleFilterView(FilterView):
    model = Article
    filterset_class = ArticleFilter
    template_name = 'summarizer/article_list.html'
    context_object_name = 'articles'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['users'] = User.objects.all()
        return context

def custom_404(request, exception):
    return render(request, '404.html', status=404)

def custom_500(request):
    return render(request, '500.html', status=500)

@login_required
def delete_summary(request, article_pk, summary_pk):
    summary = get_object_or_404(Summary, pk=summary_pk)
    article_pk = summary.article.pk
    summary.delete()
    return redirect('article_detail', pk=article_pk)


@login_required
def delete_article(request, pk):
    article = get_object_or_404(Article, pk=pk)
    article.delete()
    return redirect('index')


@login_required
def index(request):
    articles = Article.objects.filter(user=request.user)
    return render(request, 'summarizer/index.html', {'articles': articles})

@login_required
def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    return render(request, 'summarizer/article_detail.html', {'article': article})

@login_required
def add_article(request):
    if request.method == 'POST':
        article_form = ArticleForm(request.POST)
        category_form = CategoryForm(request.POST)
        
        # Vérifier si l'article est valide et enregistrer
        if article_form.is_valid():
            article = article_form.save(commit=False)
            article.user = request.user
            
            # Vérifier si une catégorie a été sélectionnée ou ajoutée
            if 'category' in request.POST and request.POST['category']:
                category = Category.objects.get_or_create(name=request.POST['category'])[0]
                article.category = category
            
            article.save()
            return redirect('index')
    else:
        article_form = ArticleForm()
        category_form = CategoryForm()
    
    return render(request, 'summarizer/add_article.html', {'article_form': article_form, 'category_form': category_form})

@login_required
def generate_summary(request, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        language = request.POST.get('language', 'en')  # Langue sélectionnée par l'utilisateur

        model = ChatOpenAI(api_key=OPENAI_API_KEY)
        parser = PydanticOutputParser(pydantic_object=SummaryModel)

        # Template générique pour résumer un article dans différentes langues
        TEMPLATE_PROMPT = """
        Summarize the following article content:

        \n{format_instructions}\n{content}\n

        Key points:
        - Main subject and context of the article.
        - Significant events or achievements discussed.
        - Important insights or conclusions drawn.
        """

        prompt = PromptTemplate(
            template=TEMPLATE_PROMPT,
            input_variables=["content"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )

        chain = prompt | model | parser

        try:
            summary_content = chain.invoke({"content": article.content})

            # Déterminer le texte du résumé en fonction de la langue
            summary_text = getattr(summary_content, f"summary_text_{language}", None)
            if not summary_text:
                summary_text = summary_content.summary_text_en  # Fallback to English if language-specific summary is not available

            # Sauvegarder le résumé en base de données
            Summary.objects.create(article=article, summary_text=summary_text)
            return redirect('article_detail', pk=article.pk)

        except Exception as e:
            logging.error(f"Erreur lors de la génération du résumé : {e}")
            return JsonResponse({'error': str(e)}, status=500)

    return render(request, 'summarizer/generate_summary.html', {'article': article})