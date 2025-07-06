from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import *
from .views import (
    UserViewSet, ProfileViewSet, PatientNutritionistViewSet, ScanViewSet,
    TaskViewSet, RecipeViewSet, ScanRecipeSuggestionViewSet, ProgressLogViewSet,
    register_user, CustomTokenObtainPairView  # 👈 IMPORTANTE
)

router = DefaultRouter()
router.register('users', UserViewSet)
router.register('profiles', ProfileViewSet)
router.register('patient-nutritionists', PatientNutritionistViewSet)
router.register('scans', ScanViewSet)
router.register('tasks', TaskViewSet)
router.register('recipes', RecipeViewSet)
router.register('scan-recipe-suggestions', ScanRecipeSuggestionViewSet)
router.register('progress-logs', ProgressLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/', register_user),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),  # 👈 Refresh # ✅ Asegúrate de que core/urls.py exista
]