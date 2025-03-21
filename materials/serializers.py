from rest_framework.serializers import ModelSerializer, SerializerMethodField
from rest_framework import serializers
from materials.models import Course, Lesson, Subscription
from .validators import youtube_link_validator

class LessonSerializer(ModelSerializer):
    video_link = serializers.URLField(
        validators=[youtube_link_validator],  # Валидатор для поля video_link
        required=False
    )

    class Meta:
        model = Lesson
        fields = "__all__"
        read_only_fields = ['owner']


class CourseSerializer(ModelSerializer):
    is_subscribed = serializers.SerializerMethodField()
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only= True, source='lesson_set')
    video_link = serializers.URLField(
        validators=[youtube_link_validator],  # Валидатор для поля video_link
        required=False
    )


    def get_lesson_count(self, course):
        return course.lesson_set.count()

    def get_is_subscribed(self, obj):
        """Проверяем, есть ли у текущего пользователя подписка на курс"""
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            return Subscription.objects.filter(user=request.user, course=obj).exists()
        return False




    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lesson_count', 'lessons', 'video_link', 'is_subscribed']





