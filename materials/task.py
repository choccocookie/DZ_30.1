from celery import shared_task
from django.core.mail import send_mail
from django.utils.timezone import now, timedelta
from .models import Subscription, Course

@shared_task
def send_course_update_emails(course_id):
    course = Course.objects.get(id=course_id)
    subscribers = Subscription.objects.filter(course=course)

    if course.updated_at < now() - timedelta(hours=4):
        for sub in subscribers:
            send_mail(
                "Обновление курса",
                f"Курс '{course.name}' был обновлен. Проверьте новые материалы!",
                "from@example.com",
                [sub.user.email],
            )
