from rest_framework.serializers import ModelSerializer, SerializerMethodField

from system.models import User, Payment
from rest_framework import serializers


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"


class UserSerializer(ModelSerializer):
    payments = PaymentSerializer(many=True, source="payment_set", read_only=True)
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ["id", "email", "phone", "сity", "avatar", "payments", "password"]

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

