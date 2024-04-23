from rest_framework import pagination


class CoursePaginator(pagination.PageNumberPagination):
    page_size = 3


class CommentPaginator(pagination.PageNumberPagination):
    page_size = 2