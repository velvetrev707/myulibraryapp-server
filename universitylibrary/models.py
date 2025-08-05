from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.utils import timezone

class User(AbstractUser):
    """
    Custom user model that extends Django's AbstractUser.
    This model can be extended with additional fields if needed.
    """
    # Define user types
    STUDENT = 'student'
    LIBRARIAN = 'librarian'

    USER_TYPE_CHOICES = (
        (STUDENT, 'Student'),
        (LIBRARIAN, 'Librarian'),
    )

    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=STUDENT)
    email = models.EmailField(unique=True)

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name="library_user_groups"
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name="library_user_permissions"
    )

class Book(models.Model):
    """
    Model representing a book in the library.
    """

    # Default genre
    DEFAULT_GENRE = 'Fiction'

    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(max_length=50, default=DEFAULT_GENRE)
    isbn = models.CharField(max_length=13, unique=True)
    total_copies = models.PositiveIntegerField(default=1)
    available_copies = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.title

class Checkout(models.Model):
    """
    Model representing a checkout record for a book.
    """
    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name='checkouts')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    checkout_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)
    is_returned = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Update book availability when checkout status changes
        if not self.pk:  # New checkout
            self.book.available_copies -= 1
        elif self.is_returned and not self.return_date:
            self.book.available_copies += 1
            self.return_date = timezone.now()
        self.book.save()
        super().save(*args, **kwargs)

class BorrowRecord(models.Model):
    """
    Model representing a record of a book borrowed by a user.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    borrow_date = models.DateTimeField(auto_now_add=True)
    return_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} borrowed {self.book.title}"


