from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Review, UserProfile, ReviewLike, ReviewComment

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


# User Profile Serializer
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['bio', 'avatar']

# Review Like Serializer
class ReviewLikeSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = ReviewLike
        fields = ['id', 'user', 'created_at']

# Review Comment Serializer
class ReviewCommentSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    class Meta:
        model = ReviewComment
        fields = ['id', 'user', 'content', 'created_at']

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    likes_count = serializers.SerializerMethodField()
    comments = ReviewCommentSerializer(many=True, read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'movie_title', 'review_content', 'rating', 'user', 'created_date', 'likes_count', 'comments']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def create(self, validated_data):
        # Handle creation for both authenticated and anonymous users
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)
