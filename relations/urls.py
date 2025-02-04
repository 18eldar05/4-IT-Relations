from django.contrib import admin
from django.urls import path, include
from users import views
from library import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('', include('library.urls')),
]
