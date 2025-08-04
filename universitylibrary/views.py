from django.shortcuts import render

from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import User, Book, Checkout
from .serializers import UserSerializer, BookSerializer, CheckoutSerializer
from .permissions import IsLibrarian, IsStudent

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['genre', 'author']
    search_fields = ['title', 'author', 'genre']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsLibrarian()]
        return [permissions.IsAuthenticated()]

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

    @action(detail=True, methods=['post'], permission_classes=[IsStudent])
    def checkout(self, request, pk=None):
        book = self.get_object()
        if book.available_copies <= 0:
            return Response({'error': 'No available copies'}, status=status.HTTP_400_BAD_REQUEST)

        checkout = Checkout.objects.create(
            student=request.user,
            book=book
        )

        #super().checkout(request, pk)
        return Response(CheckoutSerializer(checkout).data, status=status.HTTP_201_CREATED)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsLibrarian]

    def list(self, request, *args, **kwargs):
        print("******* Listing all users *******")
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        print("******* Creating a new user *******")
        return super().create(request, *args, **kwargs)

class CheckoutViewSet(viewsets.ModelViewSet):
    serializer_class = CheckoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'librarian':
            return Checkout.objects.all()
        return Checkout.objects.filter(student=user)

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @action(detail=True, methods=['post'], permission_classes=[IsLibrarian])
    def return_book(self, request, pk=None):
        checkout = self.get_object()
        if checkout.is_returned:
            return Response({'error': 'Book already returned'}, status=status.HTTP_400_BAD_REQUEST)

        checkout.is_returned = True
        checkout.save()
        return Response(self.get_serializer(checkout).data)
