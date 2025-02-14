from django.urls import path
from library.views import *

urlpatterns = [
    path('api/genre/', GenreCreateView.as_view(), name="genre"),
    path('api/genre/<int:pk>/', GenreView.as_view(), name="genre_pk"),
    path('api/author/', AuthorCreateView.as_view(), name="author"),
    path('api/author/<int:pk>/', AuthorView.as_view(), name="author_pk"),
    path('api/book/', BookCreateView.as_view(), name="book"),
    path('api/book/<int:pk>/', BookView.as_view(), name="book_pk"),
    path('api/reading_room/', ReadingRoomCreateView.as_view(), name="reading_room"),
    path('api/reading_room/<int:pk>/', ReadingRoomView.as_view(), name="reading_room_pk"),
    path('api/take_the_book/<int:pk>/', IssuanceCreateView.as_view(), name="take_the_book"),
    path('api/return_the_book/<int:pk>/', ReturnView.as_view(), name="return_the_book"),
    path('api/debt/<int:pk>/', DebtView.as_view(), name="debt"),
    path('api/notify/', NotifyView.as_view(), name="notify"),
]
