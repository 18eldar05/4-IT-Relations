from django.contrib import admin
from .models import *
from unfold.admin import ModelAdmin
from unfold.contrib.filters.admin import RangeDateFilter, FieldTextFilter, RelatedDropdownFilter


@admin.register(ReadingRoom)
class ReadingRoomAdmin(ModelAdmin):
    change_form_show_cancel_button = True


@admin.register(Book)
class BookAdmin(ModelAdmin):
    list_display = ("name", "author", "genre", "is_taken")
    compressed_fields = True
    list_filter_submit = True
    list_filter_sheet = False
    list_disable_select_all = False
    list_fullwidth = True
    change_form_show_cancel_button = True
    list_filter = (
        ("name", FieldTextFilter),
        ("author", RelatedDropdownFilter),
        ("genre", RelatedDropdownFilter),
        ("reading_room", RelatedDropdownFilter),
    )


@admin.register(Author)
class AuthorAdmin(ModelAdmin):
    change_form_show_cancel_button = True


@admin.register(Genre)
class GenreAdmin(ModelAdmin):
    change_form_show_cancel_button = True


@admin.register(Issuance)
class IssuanceAdmin(ModelAdmin):
    list_display = ("reader", "book", "date_of_issue", "date_of_return", "is_returned")
    compressed_fields = False
    change_form_show_cancel_button = True
    list_filter_submit = True
    list_filter_sheet = False
    list_filter = (
        ("date_of_issue", RangeDateFilter),
        ("date_of_return", RangeDateFilter),
        ("reader", RelatedDropdownFilter),
        ("book", RelatedDropdownFilter),
    )
