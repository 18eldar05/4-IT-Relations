from rest_framework import serializers
from library.models import *


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class ReadingRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReadingRoom
        fields = '__all__'


class IssuanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issuance
        fields = '__all__'


class DebtSerializer(serializers.ModelSerializer):
    class Meta:
        model = Issuance
        fields = ['book', 'date_of_return']
