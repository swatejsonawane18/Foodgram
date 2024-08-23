from django.contrib import admin
from .models import Seller, Post, Like

@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('seller', 'description', 'price', 'created_at')

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'created_at')
