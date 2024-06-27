from django.test import TestCase, Client
from django.contrib.auth.models import User
from .models import Article, Summary, Category
from django.urls import reverse
from unittest.mock import patch
import logging

class CategoryModelTest(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name='Test Category')

    def test_category_creation(self):
        category = Category.objects.get(id=self.category.id)
        self.assertEqual(category.name, 'Test Category')

class ArticleModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.article = Article.objects.create(title='Test Article', content='Test content', user=self.user, category=self.category)

    def test_article_creation(self):
        article = Article.objects.get(id=self.article.id)
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.content, 'Test content')
        self.assertEqual(article.user.username, 'testuser')
        self.assertEqual(article.category.name, 'Test Category')

class SummaryModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.article = Article.objects.create(title='Test Article', content='Test content', user=self.user, category=self.category)
        self.summary = Summary.objects.create(article=self.article, summary_text='Test summary')

    def test_summary_creation(self):
        summary = Summary.objects.get(id=self.summary.id)
        self.assertEqual(summary.summary_text, 'Test summary')
        self.assertEqual(summary.article.title, 'Test Article')

class ArticleViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.category = Category.objects.create(name='Test Category')
        self.article = Article.objects.create(title='Test Article', content='Test content', user=self.user, category=self.category)

    def test_article_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')

    def test_article_detail_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('article_detail', args=[self.article.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Article')
        self.assertContains(response, 'Test content')

    def test_generate_summary_view_redirects_for_anonymous_user(self):
        response = self.client.get(reverse('generate_summary', args=[self.article.id]))
        self.assertEqual(response.status_code, 302)  # Redirect to login

    @patch('summarizer.views.ChatOpenAI')
    def test_generate_summary_view(self, MockChatOpenAI):
        self.client.login(username='testuser', password='testpassword')

        mock_model = MockChatOpenAI.return_value
        mock_model.invoke.return_value = {'summary_text': 'This is a test summary'}

        response = self.client.post(reverse('generate_summary', args=[self.article.id]))

        # Ajout de journaux de débogage
        logging.debug(f'Response status code: {response.status_code}')
        logging.debug(f'Response content: {response.content.decode("utf-8")}')

        self.assertEqual(response.status_code, 302)  # Redirect to article detail
        self.assertTrue(Summary.objects.filter(article=self.article).exists())
