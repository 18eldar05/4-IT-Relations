from django.test import TestCase
from django.urls import reverse
from library.models import *
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class Test(TestCase):
    def setUp(self):
        self.author = Author.objects.create(first_name='John', last_name='Smith', country='Belarus')
        self.genre = Genre.objects.create(name='Test genre')
        self.reading_room = ReadingRoom.objects.create(name='My Library', city='Belgrade', street='Pushkina', house_number='8/2')
        self.book = Book.objects.create(name='Book Name', author=self.author, genre=self.genre, reading_room=self.reading_room)
        self.book2 = Book.objects.create(name='Book 2nd', author=self.author, genre=self.genre, reading_room=self.reading_room)
        self.book3 = Book.objects.create(name='Book 3rd', author=self.author, genre=self.genre, reading_room=self.reading_room)
        self.admin_user = User.objects.create_user(username='admin_user', password='12345', role='admin')
        self.admin_user.save()
        self.admin_access = str(RefreshToken.for_user(self.admin_user).access_token)
        self.reader_user = User.objects.create_user(username='reader_user', password='12345')
        self.reader_user.save()
        self.reader_access = str(RefreshToken.for_user(self.reader_user).access_token)
        self.book4 = Book.objects.create(is_taken=True, name='4', author=self.author, genre=self.genre, reading_room=self.reading_room)
        Issuance.objects.create(reader=self.reader_user, book=self.book4, date_of_return="2025-04-13T12:00")

    def test_safe_methods(self):
        resp = self.client.get(reverse('genre_pk', kwargs={'pk': self.genre.pk}))
        self.assertEqual(resp.status_code, 200, "genre_pk error")
        resp = self.client.get(reverse('author_pk', kwargs={'pk': self.author.pk}))
        self.assertEqual(resp.status_code, 200, "author_pk error")
        resp = self.client.get(reverse('book_pk', kwargs={'pk': self.book.pk}))
        self.assertEqual(resp.status_code, 200, "book_pk error")
        resp = self.client.get(reverse('reading_room_pk', kwargs={'pk': self.reading_room.pk}))
        self.assertEqual(resp.status_code, 200, "reading_room_pk error")

    def test_create_author(self):
        resp = self.client.post(reverse('author'), {
            "first_name": "Fn",
            "last_name": "Ln",
            "country": "Co",
        }, headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 201)

    def test_create_genre(self):
        resp = self.client.post(reverse('genre'), {
            "name": "Tg",
        }, headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 201)

    def test_create_reading_room(self):
        resp = self.client.post(reverse('reading_room'), {
            "name": "Rn",
            "city": "Ci",
            "street": "St",
            "house_number": "4/3",
        }, headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 201)

    def test_create_book(self):
        resp = self.client.post(reverse('book'), {
            "name": "Bn",
            "author": self.author.pk,
            "genre": self.genre.pk,
            "reading_room": self.reading_room.pk,
        }, headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 201)

    def test_delete_book(self):
        resp = self.client.delete(reverse('book_pk', kwargs={'pk': self.book2.pk}))
        self.assertEqual(resp.status_code, 401)
        resp = self.client.delete(reverse('book_pk', kwargs={'pk': self.book2.pk}),
                                  headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 403)
        resp = self.client.delete(reverse('book_pk', kwargs={'pk': self.book2.pk}),
                                  headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 204)

    def test_update_reading_room(self):
        resp = self.client.patch(reverse('reading_room_pk', kwargs={'pk': self.reading_room.pk}), {"name": "New Name"},
                                 content_type="application/json")
        self.assertEqual(resp.status_code, 401)
        resp = self.client.patch(reverse('reading_room_pk', kwargs={'pk': self.reading_room.pk}), {"name": "New Name"},
                                 content_type="application/json", headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 403)
        resp = self.client.patch(reverse('reading_room_pk', kwargs={'pk': self.reading_room.pk}), {"name": "New Name"},
                                 content_type="application/json", headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 200)

    def test_debt(self):
        resp = self.client.get(reverse('debt', kwargs={'pk': self.reader_user.pk}))
        self.assertEqual(resp.status_code, 401)
        resp = self.client.get(reverse('debt', kwargs={'pk': self.reader_user.pk}),
                               headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 200, "reader sees himself")
        resp = self.client.get(reverse('debt', kwargs={'pk': self.admin_user.pk}),
                               headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 204)
        resp = self.client.get(reverse('debt', kwargs={'pk': self.reader_user.pk}),
                               headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 200, "admin sees reader")
        resp = self.client.get(reverse('debt', kwargs={'pk': self.admin_user.pk}),
                               headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 403)

    def test_issuance(self):
        resp = self.client.post(reverse('take_the_book', kwargs={'pk': self.book.pk}), {
            "reader": self.admin_user.pk,
            "date_of_return": "2025-04-13T12:00"
        })
        self.assertEqual(resp.status_code, 401)

        resp = self.client.post(reverse('take_the_book', kwargs={'pk': self.book.pk}), {
            "reader": self.admin_user.pk,
            "date_of_return": "2025-04-13T12:00"
        }, headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 403)

        resp = self.client.post(reverse('take_the_book', kwargs={'pk': self.book.pk}), {
            "date_of_return": "2025-04-13T12:00"
        }, headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 201, "reader takes book for himself")

        resp = self.client.post(reverse('take_the_book', kwargs={'pk': self.book.pk}), {
            "date_of_return": "2025-04-13T12:00"
        }, headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 400)

        resp = self.client.post(reverse('take_the_book', kwargs={'pk': self.book3.pk}), {
            "reader": self.reader_user.pk,
            "date_of_return": "2025-04-13T12:00"
        }, headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 201, "admin takes book for reader")

    def test_return(self):
        resp = self.client.post(reverse('return_the_book', kwargs={'pk': self.book4.pk}),
                                headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 403)
        resp = self.client.post(reverse('return_the_book', kwargs={'pk': self.book4.pk}),
                                headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.post(reverse('return_the_book', kwargs={'pk': self.book4.pk}),
                                headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 400)
