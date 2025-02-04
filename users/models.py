from django.db import models
from library.models import ReadingRoom
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    class ChoiceRole(models.TextChoices):
        reader = "reader"
        librarian = "librarian"
        admin = "admin"
    role = models.CharField(max_length=9, choices=ChoiceRole, default=ChoiceRole.reader)
    reading_room = models.ForeignKey(ReadingRoom, null=True, on_delete=models.PROTECT)
