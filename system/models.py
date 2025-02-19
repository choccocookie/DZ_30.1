from django.contrib.auth.models import AbstractUser
from django.db import models
from materials.models import Course, Lesson


class User(AbstractUser):
    username = None
    email = models.EmailField(
        unique=True, verbose_name="Почта", help_text="Укажите почту"
    )
    phone = models.CharField(
        max_length=35,
        blank=True,
        null=True,
        verbose_name="Телефон",
        help_text="Укажите телефон",
    )
    сity = models.CharField(
        max_length=50,
        verbose_name="Город",
        help_text="Укажите город или иной населенный пункт",
    )
    avatar = models.ImageField(
        upload_to="users/avatars",
        blank=True,
        null=True,
        verbose_name="Аватар",
        help_text="Укажите аватар",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"

class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Наличные'),
        ('transfer', 'Перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    date = models.DateField(verbose_name="Дата оплаты")
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Купленые курсы")
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Купленые уроки")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)

    def __str__(self):
        return f"Payment by {self.user.username} on {self.date}"


