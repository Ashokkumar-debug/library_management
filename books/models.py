from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.timezone import now

class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    genre = models.CharField(
        max_length=50,
        choices=[
            ('Fiction', 'Fiction'),
            ('Non-Fiction', 'Non-Fiction'),
            ('Sci-Fi', 'Sci-Fi'),
            ('Biography', 'Biography')
        ]
    )
    publication_year = models.PositiveIntegerField(
        default=1900,
        validators=[MinValueValidator(1900)]  
    )
    available_copies = models.PositiveIntegerField(default=0)
    isbn = models.CharField(max_length=13, validators=[MinValueValidator(10)], unique=True)
    rating = models.FloatField(
        default=1.0,
        validators=[
            MinValueValidator(1.0),  
            MaxValueValidator(5.0)  
        ]
    )
    is_featured = models.BooleanField(default=False) 
    status = models.CharField(max_length=20, choices=[('available', 'Available'), ('lost', 'Lost')], default='available')
    is_lost = models.BooleanField(default=False) 
    def __str__(self):
        return self.title

class Member(models.Model):
    MEMBERSHIP_CHOICES = [
        ('Basic', 'Basic'),
        ('Premium', 'Premium'),
        ('Elite', 'Elite')
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=10, unique=True)
    membership_start_date = models.DateField(auto_now_add=True)
    membership_type = models.CharField(max_length=10, choices=MEMBERSHIP_CHOICES)
    max_books_allowed = models.PositiveIntegerField(default=2)

    def save(self, *args, **kwargs):
        if self.membership_type == 'Basic':
            self.max_books_allowed = 2
        elif self.membership_type == 'Premium':
            self.max_books_allowed = 5
        elif self.membership_type == 'Elite':
            self.max_books_allowed = 10
        super().save(*args, **kwargs)

    def _str_(self):
        return self.name

from django.db import models
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.conf import settings

class Transaction(models.Model):
    STATUS_CHOICES = [
        ('Issued', 'Issued'),
        ('Returned', 'Returned'),
        ('Overdue', 'Overdue'),
        ('Lost', 'Lost'),
    ]
    member = models.ForeignKey('Member', on_delete=models.CASCADE)
    book = models.ForeignKey('Book', on_delete=models.CASCADE)
    issue_date = models.DateField()
    return_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    fine_amount = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    note = models.TextField(blank=True, null=True)
    action = models.CharField(max_length=50, default="Pending") 

    
    
    def clean(self):
        if not self.issue_date or not self.return_date:
            raise ValidationError("Both issue date and return date must be provided.")
        
        if self.return_date <= self.issue_date:
            raise ValidationError("Return date must be later than issue date.")
        
        if self.book.available_copies == 0 and self.status == 'Issued':
            raise ValidationError("This book is currently unavailable for borrowing.")
        
        if self.status == 'Overdue':
            self.calculate_overdue_fine()

    def calculate_overdue_fine(self):
        due_date = self.issue_date + timedelta(days=30)
        
        if self.return_date > due_date:
            overdue_days = (self.return_date - due_date).days

            if overdue_days > 0:
                self.fine_amount = overdue_days * 2
            else:
                self.fine_amount = 0
        else:
            self.fine_amount = 0

        self.send_overdue_email()

    def send_overdue_email(self):
        if self.fine_amount > 0:
            send_mail(
                'Overdue Book Notification',
                f'Dear {self.member.name},\n\nYour borrowed book "{self.book.title}" is overdue. '
                f'Fine Amount: ${self.fine_amount}. Please return it as soon as possible.\n\nThank you!',
                settings.DEFAULT_FROM_EMAIL,
                [self.member.email],
                fail_silently=False,
            )
            print(f"Overdue email sent to {self.member.email}. Fine: ${self.fine_amount}")

    def save(self, *args, **kwargs):
        self.full_clean()

        if self.status == 'Issued' and self.return_date < self.issue_date:
            self.status = 'Overdue'

        if self.status == 'Issued':
            if self.book.available_copies > 0:
                self.book.available_copies -= 1
                self.book.save()
            else:
                raise ValidationError("Not enough available copies to issue the book.")

        elif self.status == 'Returned':
            self.book.available_copies += 1
            self.book.save()

        if self.status == 'Overdue':
            self.calculate_overdue_fine()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.member.name} - {self.book.title}'
    
class Staff(models.Model):
    ROLE_CHOICES = [
        ('Librarian', 'Librarian'),
        ('Assistant', 'Assistant')
    ]
    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    phone_number = models.CharField(max_length=10)
    
    class Meta:
        permissions = [
            ("can_issue_books", "Can issue books"),
            ("can_return_books", "Can return books"),
            ("can_view_books_members", "Can view books and members"),
        ]

    def _str_(self):
        return self.name
