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
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment(request, course_id):
    """Создание оплаты курса через Stripe"""
    course = get_object_or_404(Course, id=course_id)

    payment = Payment.objects.create(
        user= request.user,
        course=course,
        amount=course.price,
        status="pending"
    )

    product_id = create_product(course.name)
    price_id = create_price(product_id, course.price)

    success_url = "http://localhost:8000/success/"
    cancel_url = "http://localhost:8000/cancel/"

    session_id, session_url = create_checkout_session(price_id, success_url, cancel_url)

    payment.stripe_session_id = session_id
    payment.stripe_payment_url = session_url
    payment.save()

    return JsonResponse({"session_url": session_url})