# Generated by Django 5.1.1 on 2025-01-02 08:03

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(max_length=255)),
                ('genre', models.CharField(choices=[('Fiction', 'Fiction'), ('Non-Fiction', 'Non-Fiction'), ('Sci-Fi', 'Sci-Fi'), ('Biography', 'Biography')], max_length=50)),
                ('publication_year', models.PositiveIntegerField(default=1900, validators=[django.core.validators.MinValueValidator(1900)])),
                ('available_copies', models.PositiveIntegerField(default=0)),
                ('isbn', models.CharField(max_length=13, unique=True, validators=[django.core.validators.MinValueValidator(10)])),
                ('rating', models.FloatField(default=1.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)])),
            ],
        ),
        migrations.CreateModel(
            name='Member',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=10, unique=True)),
                ('membership_start_date', models.DateField(auto_now_add=True)),
                ('membership_type', models.CharField(choices=[('Basic', 'Basic'), ('Premium', 'Premium'), ('Elite', 'Elite')], max_length=10)),
                ('max_books_allowed', models.PositiveIntegerField(default=2)),
            ],
        ),
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('role', models.CharField(choices=[('Librarian', 'Librarian'), ('Assistant', 'Assistant')], max_length=50)),
                ('phone_number', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('issue_date', models.DateField()),
                ('return_date', models.DateField()),
                ('status', models.CharField(choices=[('Issued', 'Issued'), ('Returned', 'Returned'), ('Overdue', 'Overdue'), ('Lost', 'Lost')], max_length=10)),
                ('fine_amount', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('note', models.TextField(blank=True, null=True)),
                ('book', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.book')),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='books.member')),
            ],
        ),
    ]
