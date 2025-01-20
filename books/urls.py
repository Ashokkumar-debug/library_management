from django.urls import path
from . import views  
from .views import add_member, member_list
from .views import add_member, member_list2
from .views import add_transaction, transaction_list

urlpatterns = [
    path('', views.login_view, name="login"),
    path("main/", views.main, name="main"),
    path('books/', views.book_list, name='book_list'),
    path("user_dashboard/", views.user_dashboard, name="user_dashboard"),
    path('books2/', views.book_list2, name='book_list2'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),
    path('books/update/<int:book_id>/', views.update_book, name='update_book'),
    path('members/add/', add_member, name='add_member'),
    path('members/', member_list, name='member_list'),
    path('members2/', member_list2, name='member_list2'),
   path('transactions/', views.transaction_list, name='transaction_list'),
    path('add-transaction/', views.add_transaction, name='add_transaction'),
    path('add_staff/', views.add_staff, name='add_staff'),
    path('staff/', views.staff_list, name='staff_list'),
    path('report/', views.report, name='report'),
    path('genre-chart/',  views.genre_popularity_chart, name='genre_chart'),
    path('top_members_report/', views.top_members_report, name='top_members_report'),
    path('mark-as-featured/<int:book_id>/', views.mark_as_featured, name='mark_as_featured'),
    path('featured_books_report/', views.featured_books_report, name='featured_books_report'),
    path('books/<int:book_id>/mark-as-lost/', views.mark_as_lost, name='mark_as_lost'),
]
