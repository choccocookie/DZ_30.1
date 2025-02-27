from rest_framework.routers import SimpleRouter
from django.urls import path, include
from system.views import PaymentViewSet, UserViewSet
from system.apps import SystemConfig
from .views import RegisterUserView




jwt_views = __import__("rest_framework_simplejwt.views", fromlist=["TokenObtainPairView"])
TokenObtainPairView = jwt_views.TokenObtainPairView
TokenRefreshView = jwt_views.TokenRefreshView
TokenVerifyView = jwt_views.TokenVerifyView

app_name = SystemConfig.name

router = SimpleRouter()
router.register("payments", PaymentViewSet)
router.register("users", UserViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('register/', RegisterUserView.as_view(), name='register'),

]

