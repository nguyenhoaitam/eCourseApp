from rest_framework import viewsets, generics, status, parsers, permissions, request
from rest_framework.decorators import action
from rest_framework.response import Response
from courses.models import Category, Course, Lesson, User, Comment, Like
from courses import serializers, paginators, perms


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializers.CategorySerializer


class CourseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Course.objects.filter(active=True)
    serializer_class = serializers.CourseSerializer
    pagination_class = paginators.CoursePaginator

    def get_queryset(self):  # Tìm kiếm theo từ khóa và id
        queryset = self.queryset

        q = self.request.query_params.get('q')
        if q:
            queryset = queryset.filter(name__icontains=q)

        cate_id = self.request.query_params.get('category_id')
        if cate_id:
            queryset = queryset.filter(category_id=cate_id)

        return queryset

    @action(methods=['get'], url_path='lessons', detail=True)
    def get_lessons(self, request, pk):  # Lấy danh sách bài học của một khóa học(Lấy dựa vào API khóa học)
        lessons = self.get_object().lesson_set.filter(active=True)  # Trả về đối tượng khóa học

        q = request.query_params.get('q')
        if q:
            lessons = lessons.filter(subject__icontains=q)

        return Response(serializers.LessonSerializer(lessons, many=True).data,
                        status=status.HTTP_200_OK)


class LessonViewSet(viewsets.ViewSet, generics.RetrieveAPIView):  # Xem chi tiết một bài học bao gồm thông tin bài học và các tag gán cho bài học.(Many to many)
    # Thực hiện join vào Tag lấy Tag ra ngay lần truy vấn đầu tiên, giúp truy vấn tốt hơn
    queryset = Lesson.objects.prefetch_related('tags').filter(active=True)
    serializer_class = serializers.LessonDetailsSerializer

    def get_serializer_class(self):
        if self.request.user.is_authenticated:
            return serializers.AuthenticatedLessonDetailsSerializer

        return self.serializer_class

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    # Lấy danh sách các comment của một bài học
    @action(methods=['get'], url_path='comments', detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').all()  # Truy vấn 1 lần

        # Phân trang comment
        paginator = paginators.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comments, many=True).data,
                        status=status.HTTP_200_OK)

    # Thêm bình luận
    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = self.get_object().comment_set.create(content=request.data.get('content'),
                                                 user=request.user)

        return Response(serializers.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    # Thích bài học
    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        li, created = Like.objects.get_or_create(lesson=self.get_object(),
                                                 user=request.user)

        if not created:
            li.active = not li.active
            li.save()

        return Response(serializers.LessonSerializer(self.get_object()).data)


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]  # Nhận file

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    # Lấy thông tin người dùng hiện tại
    # Cập nhật thông tin người dùng
    @action(methods=['get', 'patch'], url_path='current_user', detail=False)
    def current_user(self, request):
        user = request.user

        if request.method.__eq__('PATCH'):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)


# Xóa comment
class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializers.CommentSerializer
    permission_class = [perms.CommentOwner]
