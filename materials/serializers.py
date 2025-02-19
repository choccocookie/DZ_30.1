from rest_framework.serializers import ModelSerializer, SerializerMethodField

from materials.models import Course, Lesson


class LessonSerializer(ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class CourseSerializer(ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(many=True, read_only= True, source='lesson_set')


    def get_lesson_count(self, course):
        return course.lesson_set.count()



    class Meta:
        model = Course
        fields = ['id', 'name', 'description', 'preview', 'lesson_count', 'lessons']




