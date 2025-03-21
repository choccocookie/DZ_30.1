from django.db import models
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from system.models import User


#from django.contrib.auth import get_user_model
#User = get_user_model()
import system.models


class Course(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название курса", help_text="Введите название курса"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание курса",
        help_text="Введите название курса",
    )
    preview = models.ImageField(
        upload_to="materials/photo",
        blank=True,
        null=True,
        verbose_name="Превью курса",
        help_text="Загрузите превью курса",
    )
    link_to_video = models.URLField(blank=True, null=True)

    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    name = models.CharField(
        max_length=50, verbose_name="Название урока", help_text="Введите название урока"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Описание урока",
        help_text="Введите название урока",
    )
    preview = models.ImageField(
        upload_to="materials/photo",
        blank=True,
        null=True,
        verbose_name="Превью урока",
        help_text="Загрузите превью урока",
    )
    link_to_video = models.URLField(blank=True, null=True)
    course = models.ForeignKey(
        Course,
        on_delete=models.SET_NULL,
        verbose_name="Курс",
        help_text="Выберите курс",
        blank=True,
        null=True,
    )

    owner = models.ForeignKey("system.User", on_delete=models.CASCADE, related_name='lessons')

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Subscription(models.Model):
    #from system.models import User
    user = models.ForeignKey("system.User", on_delete=models.CASCADE, verbose_name='Пользователь')

    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name='Курс')

    class Meta:
        unique_together = ['user', 'course']  # Исключает дублирующие подписки
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f"{self.user.email} подписан на {self.course.title}"