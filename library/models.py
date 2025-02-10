from django.db import models
from django.contrib.auth import get_user_model


class ReadingRoom(models.Model):
    name = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    house_number = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    name = models.CharField(max_length=255)
    author = models.ForeignKey('Author', on_delete=models.PROTECT)
    genre = models.ForeignKey('Genre', null=True, blank=True, on_delete=models.PROTECT)
    reading_room = models.ForeignKey('ReadingRoom', on_delete=models.PROTECT)
    is_taken = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    country = models.CharField(max_length=255, null=True)

    def __str__(self):
        return '%s, %s' % (self.first_name, self.last_name)


class Genre(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


User = get_user_model()


class Issuance(models.Model):
    reader = models.ForeignKey(User, on_delete=models.PROTECT)
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    date_of_issue = models.DateTimeField(auto_now_add=True)
    date_of_return = models.DateTimeField(null=True)
    is_returned = models.BooleanField(default=False)
