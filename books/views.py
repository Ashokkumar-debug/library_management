from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .models import Member
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from .models import Transaction, Member, Book
from .forms import TransactionForm
from django.contrib import messages

def book_list(request):
    books = Book.objects.all()
    return render(request, 'book_list.html', {'books': books})

def add_book(request):
    if request.method == "POST":
        title = request.POST.get('title')
        author = request.POST.get('author')
        genre = request.POST.get('genre')
        publication_year = request.POST.get('publication_year')
        isbn = request.POST.get('isbn')
        rating = request.POST.get('rating')
        available_copies = request.POST.get('available_copies')
        book = Book.objects.create(
            title=title,
            author=author,
            genre=genre,
            publication_year=publication_year,
            isbn=isbn,
            rating=rating,
            available_copies=available_copies
        )
        book.save()
        return redirect('book_list')
    publication_years = list(range(1900, 2026))  
    ratings = [1, 2, 3, 4, 5]  
    return render(request, 'add_book.html', {'years': publication_years, 'ratings': ratings})

def update_book(request, book_id):
    book = get_object_or_404(Book, id=book_id) 
    if request.method == "POST":
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.genre = request.POST.get('genre')
        book.publication_year = request.POST.get('publication_year')
        book.isbn = request.POST.get('isbn')
        book.rating = request.POST.get('rating')
        book.available_copies = request.POST.get('available_copies')
        book.save()
        return redirect('book_list') 
    return render(request, 'update_book.html', {'book': book})

def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk) 
    if request.method == "POST":
        book.delete() 
        return redirect('book_list') 
    return render(request, 'delete_book.html', {'book': book})

from django.core.mail import send_mail
def add_member(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        membership_type = request.POST.get('membership_type')
        new_member = Member(
            name=name,
            email=email,
            phone_number=phone_number,
            membership_type=membership_type
        )
        send_mail(
            subject='Welcome to the Library!',
            message=f'Hello {name},\n\nThank you for joining our library as a {membership_type} member. We are excited to have you on board!',
            from_email='ashokkumarc1208@gmail.com',
            recipient_list=[email],
            fail_silently=False,
        )
        new_member.save()
        return HttpResponse("Member added successfully!")  
    return render(request, 'add_member.html')

def member_list(request):
    members = Member.objects.all()  
    return render(request, 'member_list.html', {'members': members})

def add_transaction(request):
    if request.method == 'POST':
        member_id = request.POST.get('member')
        book_id = request.POST.get('book')
        issue_date = request.POST.get('issue_date')
        return_date = request.POST.get('return_date')
        status = request.POST.get('status')
        note = request.POST.get('note')
        member = Member.objects.get(id=member_id)
        book = Book.objects.get(id=book_id)
        transaction = Transaction(
            member=member,
            book=book,
            issue_date=issue_date,
            return_date=return_date,
            status=status,
            note=note,
        )
        try:
            transaction.full_clean()  
            transaction.save()
            messages.success(request, "Transaction added successfully!")
            return redirect('transaction_list')  
        except ValidationError as e:
            messages.error(request, str(e))  
    members = Member.objects.all()
    books = Book.objects.all()
    return render(request, 'add_transaction.html', { 
        'members': members,
        'books': books,
        
    })

def transaction_list(request):
    transactions = Transaction.objects.all()
    members = Member.objects.all()
    books = Book.objects.all()
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')  
    else:
        form = TransactionForm()
    return render(request, 'transaction_list.html', {
        'transactions': transactions,
        'members': members,
        'books': books,
        'form': form,
    })

from django.shortcuts import render, redirect
from .forms import StaffForm
from .models import Staff

def add_staff(request):
    if request.method == 'POST':
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()  
            return redirect('staff_list')  
    else:
        form = StaffForm()
    return render(request, 'add_staff.html', {'form': form})

def staff_list(request):
    staff_members = Staff.objects.all()  
    return render(request, 'staff_list.html', {'staff_members': staff_members})

credentials = {
    "micheal001@gmail.com": "123",  
    "eric122@gmail.com": "345",  
}

def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        if username in credentials and credentials[username] == password:
            if username == "micheal001@gmail.com":
                return redirect("main")  
            else:
                return redirect("user_dashboard")  
        else:
            error_message = "Invalid username or password"
            return render(request, "login.html", {"error": error_message})
    return render(request, "login.html")  

def main(request):
    return render(request, "main.html")  

def user_dashboard(request):
    return render(request, "main2.html")  

def book_list2(request):
    books2 = Book.objects.all()
    return render(request, 'book_list2.html', {'books2': books2})

def member_list2(request):
    members2 = Member.objects.all()  
    return render(request, 'member_list2.html', {'members2': members2})

from django.shortcuts import render
from .models import Book, Member, Transaction
from django.db.models import Sum, Q

def main(request):
    total_members = Member.objects.count()
    total_available_copies = Book.objects.aggregate(Sum('available_copies'))['available_copies__sum'] or 0
    total_fine_amount = Transaction.objects.filter(status='Overdue').aggregate(Sum('fine_amount'))['fine_amount__sum'] or 0
    overdue_member_count = Member.objects.filter(
        transaction__status='Overdue'
    ).distinct().count()
    return render(request, 'main.html', {
        'total_members': total_members,
        'total_available_copies': total_available_copies,
        'total_fine_amount': total_fine_amount,
        'overdue_member_count': overdue_member_count
    })

from django.shortcuts import render
from .models import Transaction

def report(request):
    overdue_transactions = Transaction.objects.filter(status='Overdue')
    overdue_members = [{
        'name': transaction.member.name,
        'email': transaction.member.email,
        'phone_number': transaction.member.phone_number,
        'fine_amount': transaction.fine_amount or 0  
    } for transaction in overdue_transactions]
    return render(request, 'report.html', {'overdue_members': overdue_members})

from django.shortcuts import render
from .models import Transaction

def genre_popularity_chart(request):
    transactions = Transaction.objects.all()
    genres = []
    for transaction in transactions:
        if transaction.book:
            genres.append(transaction.book.genre)
    genre_counts = {}
    for genre in genres:
        genre_counts[genre] = genre_counts.get(genre, 0) + 1
    genres = list(genre_counts.keys())
    counts = list(genre_counts.values())
    return render(request, 'genre_chart.html', {
        'genres': genres,
        'counts': counts
    })

from django.shortcuts import render
from django.db.models import Count
from .models import Transaction
from datetime import datetime

def top_members_report(request):
    current_month = datetime.now().month
    current_year = datetime.now().year
    top_members = Transaction.objects.filter(issue_date__month=current_month, issue_date__year=current_year) \
                                      .values('member__id', 'member__name') \
                                      .annotate(books_borrowed=Count('book')) \
                                      .order_by('-books_borrowed')[:10]
    return render(request, 'top_members_report.html', {'top_members': top_members})

from django.shortcuts import get_object_or_404, redirect
from .models import Book

def mark_as_featured(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.is_featured = not book.is_featured  
    book.save()
    return redirect('book_list')  

from django.shortcuts import render
from .models import Book

def featured_books_report(request):
    books = Book.objects.all()  
    return render(request, 'report_book_list.html', {'books': books})

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Book

def mark_as_featured(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    book.is_featured = not book.is_featured  
    book.save()
    return JsonResponse({
        'success': True,
        'is_featured': book.is_featured  
    })

from django.shortcuts import get_object_or_404, redirect
from django.utils.timezone import now
from django.contrib import messages
from .models import Book, Transaction
from django.core.exceptions import ValidationError

def mark_as_lost(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    try:
        book.is_lost = True
        book.available_copies = 0
        book.save()

        # Log the transaction
        Transaction.objects.create(
            member=None,
            book=book,
            issue_date=now(),
            return_date=now(),
            status="Lost",
            note="Book marked as lost by admin action.",
        )
    except ValidationError as e:
        messages.error(request, f"Error: {', '.join(e.messages)}")
        return redirect('book_list')  # Replace 'book_list' with your desired page

    messages.success(request, f"Book '{book.title}' marked as lost.")
    return redirect('book_list')

