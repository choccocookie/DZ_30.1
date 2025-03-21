from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets, generics
from .models import Payment, User
from .serializers import PaymentSerializer, UserSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method']
    ordering_fields = ['date']
    ordering = ['-date']


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = []

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Course
from .stripe_service import create_product, create_price, create_checkout_session

def create_payment(request, course_id):
    """Создание оплаты курса через Stripe"""
    course = get_object_or_404(Course, id=course_id)

    product_id = create_product(course.name)
    price_id = create_price(product_id, course.price)

    success_url = "http://localhost:8000/success/"
    cancel_url = "http://localhost:8000/cancel/"

    session_id, session_url = create_checkout_session(price_id, success_url, cancel_url)

    return JsonResponse({"session_url": session_url})