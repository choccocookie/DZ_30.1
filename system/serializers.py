from rest_framework.serializers import ModelSerializer, SerializerMethodField

from system.models import User, Payment


class PaymentSerializer(ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"