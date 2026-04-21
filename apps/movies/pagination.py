from apps.base.pagination import BaseCursorPagination


class MovieCursorPagination(BaseCursorPagination):
    ordering = ("-release_date", "-id")
