from rest_framework import viewsets, generics
from django.contrib.auth.models import User
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST
from rest_framework.decorators import action
from .models import Seller, Post, Like, Purchase
from .serializers import SellerSerializer, PostSerializer, LikeSerializer, PurchaseSerializer

class SellerViewSet(viewsets.ModelViewSet):
    queryset = Seller.objects.all()
    serializer_class = SellerSerializer

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        # Allow anyone to view posts (list or retrieve actions)
        if self.action in ['list', 'retrieve']:
            permission_classes = [AllowAny]
        # Require authentication to create, update, or delete posts
        else:
            permission_classes = [IsAuthenticated]
        return [permission() for permission in permission_classes]

    def perform_create(self, serializer):
        seller = Seller.objects.get(user=self.request.user)
        serializer.save(seller=seller)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def like(self, request, pk=None):
        post = self.get_object()
        user = request.user
        like, created = Like.objects.get_or_create(user=user, post=post)
        if not created:
            like.delete()  # If the like already exists, unlike it
            return Response({'status': 'unliked'})
        return Response({'status': 'liked'})

class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can like/unlike

class PurchaseViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    permission_classes = [IsAuthenticated]  # Ensure only authenticated users can purchase

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        # Return a simple message indicating payment needs to be integrated
        return Response({"message": "Payment needs to be integrated"}, status=HTTP_201_CREATED)

class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        email = request.data.get('email')
        first_name = request.data.get('first_name')
        last_name = request.data.get('last_name')

        if not username or not password or not email:
            return Response({"error": "Username, password, and email are required."}, status=HTTP_400_BAD_REQUEST)

        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=HTTP_400_BAD_REQUEST)

        user = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, last_name=last_name)
        
        # Automatically create a Seller profile for the new user
        Seller.objects.create(user=user, bio='')

        return Response({"username": user.username}, status=HTTP_201_CREATED)
