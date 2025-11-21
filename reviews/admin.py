from django.contrib import admin
from .models import Review, UserProfile, ReviewLike, ReviewComment

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('movie_title', 'rating', 'user', 'created_date')
    list_filter = ('rating', 'created_date', 'user')
    search_fields = ('movie_title', 'review_content', 'user__username')
    ordering = ('-created_date',)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'bio')

@admin.register(ReviewLike)
class ReviewLikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'review__movie_title')

@admin.register(ReviewComment)
class ReviewCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'review', 'content', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('user__username', 'review__movie_title', 'content')
    ordering = ('-created_at',)
