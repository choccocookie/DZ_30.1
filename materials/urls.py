from rest_framework.routers import SimpleRouter
from django.urls import path
from materials.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonListApiView,
    LessonRetrieveApiView,
    LessonUpdateApiView,
    LessonDestroyeApiView,
)
from materials.apps import MaterialsConfig

app_name = MaterialsConfig.name

router = SimpleRouter()
router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="LessonList"),
    path("lesson/<int:pk>/", LessonRetrieveApiView.as_view(), name="LessonRetrieve"),
    path("lesson/<int:pk>/update/", LessonUpdateApiView.as_view(), name="LessonUpdate"),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyeApiView.as_view(), name="LessonDestroy"
    ),
    path("lesson/create/", LessonCreateApiView.as_view(), name="LessonCreate"),
]

urlpatterns += router.urls
