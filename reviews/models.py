from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
	movie_title = models.CharField(max_length=255)
	review_content = models.TextField()
	rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
	user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reviews')
	created_date = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"{self.movie_title} - {self.rating}/5 by {self.user.username}"

# User Profile for additional info and listing user's reviews
class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
	bio = models.TextField(blank=True, null=True)
	avatar = models.URLField(blank=True, null=True)

	def __str__(self):
		return f"Profile of {self.user.username}"

# Likes for reviews
class ReviewLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='likes')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		unique_together = ('user', 'review')

	def __str__(self):
		return f"{self.user.username} likes review {self.review.id}"

# Comments on reviews
class ReviewComment(models.Model):
	review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f"Comment by {self.user.username} on review {self.review.id}"
