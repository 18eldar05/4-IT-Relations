from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class Test(TestCase):
    def setUp(self):
        self.admin_user = User.objects.create_user(username='admin_user', password='12345', role='admin')
        self.admin_user.save()
        self.admin_access = str(RefreshToken.for_user(self.admin_user).access_token)
        self.reader_user = User.objects.create_user(username='reader_user', password='12345')
        self.reader_user.save()
        self.reader_access = str(RefreshToken.for_user(self.reader_user).access_token)
        self.new_librarian = User.objects.create_user(username='new_librarian', password='12345')
        self.new_librarian.save()
        self.new_librarian_access = str(RefreshToken.for_user(self.new_librarian).access_token)

    def test_registration(self):
        resp = self.client.post(reverse('register'), {
            "username": "Test_user1",
            "email": "test_user1@gmail.com",
            "password": "12345",
        })
        self.assertEqual(resp.status_code, 201)

    def test_get_user(self):
        resp = self.client.get(reverse('user', kwargs={'pk': self.reader_user.pk}))
        self.assertEqual(resp.status_code, 401)
        resp = self.client.get(reverse('user', kwargs={'pk': self.reader_user.pk}),
                                headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('user', kwargs={'pk': self.reader_user.pk}),
                                headers={"Authorization": "Bearer " + self.admin_access})
        self.assertEqual(resp.status_code, 200)
        resp = self.client.get(reverse('user', kwargs={'pk': self.admin_user.pk}),
                                headers={"Authorization": "Bearer " + self.reader_access})
        self.assertEqual(resp.status_code, 403)

    def test_update_user(self):
        resp = self.client.patch(reverse('user', kwargs={'pk': self.reader_user.pk}), {"username": "user228"},
                                 headers={"Authorization": "Bearer " + self.reader_access}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.patch(reverse('user', kwargs={'pk': self.admin_user.pk}), {"username": "user228"},
                                headers={"Authorization": "Bearer " + self.reader_access}, content_type="application/json")
        self.assertEqual(resp.status_code, 403)

        resp = self.client.patch(reverse('user', kwargs={'pk': self.reader_user.pk}), {"username": "user101"},
                                headers={"Authorization": "Bearer " + self.admin_access}, content_type="application/json")
        self.assertEqual(resp.status_code, 200)

        resp = self.client.patch(reverse('user', kwargs={'pk': self.reader_user.pk}), {"role": "librarian"},
                                headers={"Authorization": "Bearer " + self.reader_access}, content_type="application/json")
        self.assertEqual(User.objects.get(pk=self.reader_user.pk).role, "reader")

    def test_role(self):
        resp = self.client.patch(reverse('role', kwargs={'pk': self.new_librarian.pk}), {"role": "librarian"},
                                headers={"Authorization": "Bearer " + self.new_librarian_access}, content_type="application/json")
        self.assertEqual(resp.status_code, 403)
        resp = self.client.patch(reverse('role', kwargs={'pk': self.new_librarian.pk}), {"role": "librarian"},
                                 headers={"Authorization": "Bearer " + self.admin_access}, content_type="application/json")
        self.assertEqual(User.objects.get(pk=self.new_librarian.pk).role, "librarian")
