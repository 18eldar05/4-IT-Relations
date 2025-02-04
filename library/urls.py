from django.urls import path
from library.views import *

urlpatterns = [
    path('api/genre/', GenreCreateView.as_view()),
    path('api/genre/<int:pk>/', GenreView.as_view()),
    path('api/author/', AuthorCreateView.as_view()),
    path('api/author/<int:pk>/', AuthorView.as_view()),
    path('api/book/', BookCreateView.as_view()),
    path('api/book/<int:pk>/', BookView.as_view()),
    path('api/reading_room/', ReadingRoomCreateView.as_view()),
    path('api/reading_room/<int:pk>/', ReadingRoomView.as_view()),
    path('api/take_the_book/<int:pk>/', IssuanceCreateView.as_view()),
    path('api/return_the_book/<int:pk>/', ReturnView.as_view()),
    path('api/debt/<int:pk>/', DebtView.as_view()),
]
