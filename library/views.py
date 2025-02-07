from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from users.permissions import *
from library.serializer import *


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
