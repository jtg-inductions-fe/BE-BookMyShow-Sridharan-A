from apps.base.pagination import BaseCursorPagination


class BookingCursorPagination(BaseCursorPagination):
    ordering = ("-created_at", "-id")
