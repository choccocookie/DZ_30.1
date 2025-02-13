from django.db import models


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

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
