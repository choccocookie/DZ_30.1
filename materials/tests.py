from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth import get_user_model
from materials.models import Lesson, Course, Subscription

User = get_user_model()

class LessonAPITestCase(APITestCase):
    def setUp(self):
        # Создаем пользователей
        self.user = User.objects.create_user(email='user@test.com', password='password123')
        self.moderator = User.objects.create_user(email='moderator@test.com', password='password123', is_staff=True)

        # Создаем курс
        self.course = Course.objects.create(
            name='Курс 1',
            description='Описание курса',
            preview='Внимание',
            link_to_video='https://www.youtube.com/watch?v=123456'
        )

        # Создаем урок
        self.lesson = Lesson.objects.create(
            name='Урок 1',
            description='Описание урока',
            preview='Внимание',
            course=self.course,
            owner=self.user
        )

        # URL-адреса для тестирования
        self.lesson_create_url = reverse('materials:LessonCreate')
        self.lesson_list_url = reverse('materials:LessonList')
        self.lesson_detail_url = reverse('materials:LessonRetrieve', kwargs={'pk': self.lesson.pk})
        self.lesson_update_url = reverse('materials:LessonUpdate', kwargs={'pk': self.lesson.pk})
        self.lesson_delete_url = reverse('materials:LessonDestroy', kwargs={'pk': self.lesson.pk})

    #Тесты CRUD для уроков

    def test_create_lesson(self):
        """Создание урока"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Новый урок", "course": self.course.id}
        response = self.client.post(self.lesson_create_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_list_lessons(self):
        """Получение списка уроков"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_lesson(self):
        """Просмотр отдельного урока"""
        self.client.force_authenticate(user=self.user)
        response = self.client.get(self.lesson_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], self.lesson.name)

    def test_update_lesson(self):
        """Обновление урока"""
        self.client.force_authenticate(user=self.user)
        data = {"name": "Обновленный урок"}
        response = self.client.put(self.lesson_update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.name, "Обновленный урок")

    def test_delete_lesson(self):
        """Удаление урока"""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.lesson_delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Lesson.objects.filter(pk=self.lesson.pk).exists())

    #Тесты подписок на курс

class SubscriptionAPITestCase(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(email='user@test.com', password='password123')
        self.course = Course.objects.create(name='Курс для подписки', description='Описание курса')

        self.subscribe_url = reverse('materials:Subscription', kwargs={'course_id': self.course.id})

    def test_subscribe_to_course(self):
        """Подписка на курс"""
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Subscription.objects.filter(user=self.user, course=self.course).exists())

    def test_unsubscribe_from_course(self):
        """Отписка от курса"""
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post(self.subscribe_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Subscription.objects.filter(user=self.user, course=self.course).exists())
