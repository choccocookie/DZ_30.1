from rest_framework.serializers import ModelSerializer, SerializerMethodField

from system.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, source="payment_set", read_only=True)
    class Meta:
        model = User
        fields = ["id", "email", "phone", "сity", "avatar", "payments"]

