from rest_framework import serializers
from .models import Seller, Post, Like, Purchase
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']

class SimpleSellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Seller
        fields = ['id', 'user']

class PostSerializer(serializers.ModelSerializer):
    seller = SimpleSellerSerializer(read_only=True)
    likes_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'seller', 'image', 'description', 'price', 'created_at', 'likes_count', 'user_has_liked']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_user_has_liked(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(user=user).exists()
        return False  # Return False if the user is not authenticated


class SellerSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    posts = PostSerializer(many=True, read_only=True)

    class Meta:
        model = Seller
        fields = ['id', 'user', 'bio', 'posts']

class LikeSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all())  # Reference post by ID

    class Meta:
        model = Like
        fields = ['id', 'user', 'post', 'created_at']

class PurchaseSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    post = PostSerializer(read_only=True)

    class Meta:
        model = Purchase
        fields = '__all__'
