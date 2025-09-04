from django.urls import reverse
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Review

class ReviewAPITestCase(APITestCase):
	def setUp(self):
		self.user = User.objects.create_user(username='testuser', password='testpass')
		self.review = Review.objects.create(
			movie_title='Inception',
			review_content='Great movie!',
			rating=5,
			user=self.user
		)

	def test_review_list(self):
		url = reverse('review-list')
		response = self.client.get(url)
		self.assertEqual(response.status_code, 200)

	def test_review_create_auth(self):
		self.client.login(username='testuser', password='testpass')
		url = reverse('review-list')
		data = {
			'movie_title': 'Interstellar',
			'review_content': 'Amazing!',
			'rating': 5
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 201)

	def test_review_create_unauth(self):
		url = reverse('review-list')
		data = {
			'movie_title': 'Dunkirk',
			'review_content': 'Good!',
			'rating': 4
		}
		response = self.client.post(url, data)
		self.assertEqual(response.status_code, 401)
