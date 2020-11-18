from django.urls import path
from . import views
from django.views.decorators.csrf import csrf_exempt

app_name = "books"

urlpatterns = [
    path('get_book_list/', views.get_book_list, name="get_book_list"),
    path('get_pop_book_list/', views.get_pop_book_list, name="get_pop_book_list"),
    path('book_detail/<int:book_pk>/', views.book_detail, name="book_detail"),
    path('book_search/', csrf_exempt(views.BookSearchView.as_view()), name='book_search'),
    path('like/', views.like_book, name='like_book'),
    path('book_auto_search/', views.book_auto_search, name='book_auto_search'),
    path('library/', views.library, name='library'),
    path('other_like_book/', views.other_like_book, name="other_like_book"),
]