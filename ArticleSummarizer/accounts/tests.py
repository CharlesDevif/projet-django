from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User

class AuthViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_register_view(self):
        # Test d'une inscription réussie
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'testpassword123',
            'password2': 'testpassword123',
            'bio': 'This is a test bio.',
            'profile_picture': '' 
        })
        self.assertEqual(response.status_code, 302)  
        self.assertTrue(User.objects.filter(username='newuser').exists())

        # Test d'une inscription échouée (mots de passe ne correspondent pas)
        response = self.client.post(reverse('register'), {
            'username': 'newuser2',
            'email': 'newuser2@example.com',
            'password1': 'testpassword123',
            'password2': 'wrongpassword',
            'bio': 'This is a test bio.',
            'profile_picture': ''  
        })
        self.assertEqual(response.status_code, 200) 
        self.assertContains(response, "The two password fields didn’t match.")
