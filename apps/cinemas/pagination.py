from rest_framework.pagination import CursorPagination


class CinemaCursorPagination(CursorPagination):
    page_size = 1
    ordering = "-created_at"
