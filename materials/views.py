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
from .permissions import IsModerator, IsOwner, IsNotModerator
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
            return [IsModerator | IsOwner]
        elif self.action in ['destroy']:
            return [IsOwner]
        elif self.action in ['create']:
            return [~IsModerator()]
        return super().get_permissions()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)  # Привязываем курс к владельцу


class LessonCreateApiView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModerator]

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
    permission_classes = [IsOwner | IsModerator]




class LessonDestroyApiView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner, IsNotModerator]




