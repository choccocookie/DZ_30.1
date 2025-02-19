from rest_framework.routers import SimpleRouter
from django.urls import path, include
from system.views import PaymentViewSet, UserViewSet
from system.apps import SystemConfig

app_name = SystemConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

