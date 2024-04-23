from rest_framework import serializers
from courses.models import Category, Course, Lesson, Tag, User, Comment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class ItemSerializer(serializers.ModelSerializer):  # Hàm trả về những thứ chung
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['image'] = instance.image.url
        return req  # Trả về đường dẫn ảnh đầy đủ


class CourseSerializer(ItemSerializer):  # Kế thừa lại hàm chung
    class Meta:
        model = Course
        fields = ['id', 'name', 'image', 'created_date']


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']


class LessonSerializer(ItemSerializer):  # Kế thừa lại hàm chung
    class Meta:
        model = Lesson
        fields = ['id', 'subject', 'image', 'created_date']


class LessonDetailsSerializer(LessonSerializer):
    tags = TagSerializer(many=True)

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['content', 'tags']


class AuthenticatedLessonDetailsSerializer(LessonDetailsSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, lesson):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return lesson.like_set.filter(active=True, user=request.user).exists()

    class Meta:
        model = LessonSerializer.Meta.model
        fields = LessonSerializer.Meta.fields + ['liked']


class UserSerializer(serializers.ModelSerializer):
    def create(self, validated_data):  # Xử lý mật khẩu
        data = validated_data.copy()
        user = User(**data)
        user.set_password(user.password)
        user.save()

        return user

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        if instance.avatar:
            rep['avatar'] = instance.avatar.url

        return rep

    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'username', 'password', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True  # Chỉ cho đăng ký chứ không hiện password ra ngoài
            }
        }


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'created_date', 'updated_date', 'user']
