from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from users.permissions import *
from library.serializer import *
from .tasks import send_notification
from functools import lru_cache
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
import json
from django.utils.timezone import now, timedelta


class GenreView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsStaffOrReadOnly,)


class AuthorView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = (IsStaffOrReadOnly,)


class BookView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = (IsStaffOrReadOnly,)


class ReadingRoomView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ReadingRoom.objects.all()
    serializer_class = ReadingRoomSerializer
    permission_classes = (IsStaffOrReadOnly,)


class GenreCreateView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    def post(self, request):
        serializer = GenreSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Genre has been created", "data": serializer.data}, status=status.HTTP_201_CREATED)


class AuthorCreateView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    def post(self, request):
        serializer = AuthorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Author has been created", "data": serializer.data}, status=status.HTTP_201_CREATED)


class BookCreateView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    def post(self, request):
        serializer = BookSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Book has been created", "data": serializer.data}, status=status.HTTP_201_CREATED)


class ReadingRoomCreateView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    def post(self, request):
        serializer = ReadingRoomSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Reading room has been created", "data": serializer.data}, status=status.HTTP_201_CREATED)


class IssuanceCreateView(APIView):
    permission_classes = (IsStaffOrOwner,)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method POST not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        request_data = request.data.copy()

        if "reader" not in request_data:
            request_data["reader"] = self.request.user.pk

        user = get_object_or_404(User, pk=request_data["reader"])
        self.check_object_permissions(request, user)

        book = get_object_or_404(Book, pk=pk)

        if book.is_taken:
            return Response({"error": "This book has already been taken"}, status=status.HTTP_400_BAD_REQUEST)

        request_data["book"] = pk
        book.is_taken = True
        book.save()

        serializer = IssuanceSerializer(data=request_data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"Book has been issued": serializer.data}, status=status.HTTP_201_CREATED)


class ReturnView(APIView):
    permission_classes = (IsStaffOrReadOnly,)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method POST not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        book = get_object_or_404(Book, pk=pk)

        try:
            issuance = book.issuance_set.latest('date_of_issue')
        except:
            return Response({"error": "Book has never been taken"}, status=status.HTTP_404_NOT_FOUND)

        if book.is_taken is False and issuance.is_returned:
            return Response({"error": "Book has already been returned"}, status=status.HTTP_400_BAD_REQUEST)

        book.is_taken = False
        book.save()
        issuance.is_returned = True
        issuance.save()
        return Response({"OK": "Book has been returned"})


class DebtView(APIView):
    permission_classes = (IsStaffOrOwner,)

    def get(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method GET not allowed"}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

        user = get_object_or_404(User, pk=pk)
        self.check_object_permissions(request, user)

        debt = Issuance.objects.filter(reader=pk, is_returned=False)

        if not debt.exists():
            return Response({"No Content": "User has no debts"}, status=status.HTTP_204_NO_CONTENT)

        return Response({"List of debts": DebtSerializer(debt, many=True).data})


class NotifyView(APIView):
    def post(self, request, *args, **kwargs):
        send_notification.delay()
        return Response({"Message": "Notifications started"})


def dashboard_callback(request, context):
    context.update(random_data())
    context.update({
        "title": "Dashboard",
        "site_header": "Django site admin",
    })
    return context


@lru_cache
def random_data():
    books = Book.objects.all()
    progress_total = 0
    progress = []
    week_total = 0
    week_ago = now() - timedelta(days=7)
    for book in books:
        number = Issuance.objects.filter(book=book).count()
        progress_total += number
        progress.append({
            "title": book.name,
            "description": number,
            "value": number * 10,
        })
        week_number = Issuance.objects.filter(book=book, date_of_issue__gte=week_ago).count()
        week_total += week_number

    all_time = now() - Issuance.objects.earliest('date_of_issue').date_of_issue
    all_dates = [now() - timedelta(days=x) for x in range(all_time.days + 2)]
    all_dates.reverse()
    short_dates_all_time = [day.strftime("%b %d") for day in all_dates]
    performance_all_time = [[0, Issuance.objects.filter(date_of_issue__date=day).count()] for day in all_dates]

    dates = [now() - timedelta(days=x) for x in range(7)]
    dates.reverse()
    short_dates_week = [day.strftime("%a %d") for day in dates]
    performance_week = [[0, Issuance.objects.filter(date_of_issue__date=day).count()] for day in dates]

    users = User.objects.all()
    top_user_amount = 0
    top_user = None
    for user in users:
        amount = Issuance.objects.filter(reader=user, date_of_issue__gte=week_ago).count()
        if amount >= top_user_amount:
            top_user_amount = amount
            top_user = user

    return {
        "kpi": [
            {
                "title": "User of the week",
                "metric": top_user,
                "footer": mark_safe(
                    f'<strong class="text-green-700 font-semibold dark:text-green-400">{top_user_amount}</strong>&nbsp;books taken'
                ),
            },
        ],
        "progress_total": progress_total,
        "progress": progress,
        "chart": json.dumps(
            {
                "labels": short_dates_all_time,
                "datasets": [
                    {
                        "label": "Label",
                        "type": "line",
                        "data": performance_all_time,
                        "borderColor": "var(--color-primary-500)",
                        "backgroundColor": "var(--color-primary-700)",
                    },
                ],
            }
        ),
        "performance": [
            {
                "title": _("Total issues of last week"),
                "metric": week_total,
                "chart": json.dumps(
                    {
                        "labels": short_dates_week,
                        "datasets": [
                            {
                                "data": performance_week,
                                "borderColor": "var(--color-primary-700)",
                            }
                        ],
                    }
                ),
            },
        ],
    }
