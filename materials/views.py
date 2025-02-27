from django.shortcuts import render

from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import (
    CreateAPIView,
    ListAPIView,
    RetrieveAPIView,
    UpdateAPIView,
    DestroyAPIView,
)
from materials.models import Course, Lesson
from materials.serializers import CourseSerializer, LessonSerializer
from .permissions import IsModerator, IsOwner
from rest_framework.permissions import IsAuthenticated


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer

    def get_permissions(self):
        """
        Ограничение прав доступа:
        - Модератор может читать и редактировать, но не удалять/создавать.
        - Обычные пользователи могут работать только со своими курсами.
        """
        if self.action in ['list', 'retrieve', 'update', 'partial_update']:
            return [IsAuthenticated(), IsModerator()]
        elif self.action in ['destroy', 'create']:
            return [IsAuthenticated()]  # Только админы
        return super().get_permissions()


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем урок к владельцу


class LessonListApiView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonRetrieveApiView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class LessonUpdateApiView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        - Модератор может редактировать любой урок.
        - Обычные пользователи могут редактировать только свои уроки.
        """
        if self.request.user.groups.filter(name="Модератор").exists():
            return [IsAuthenticated(), IsModerator()]
        return [IsAuthenticated(), IsOwner()]


class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer

    def get_permissions(self):
        """
        - Только владелец урока может его удалить.
        - Модераторы НЕ МОГУТ удалять уроки.
        """
        return [IsAuthenticated(), IsOwner()]


class LessonDestroyeApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
