from django.urls import path

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api.views import GenerateBulletPoints, GenerateSummary, UserRegistrationView

urlpatterns = [
    path("user-registration/", UserRegistrationView.as_view(), name="user-register"),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("generate-summary/", GenerateSummary.as_view(), name="generate-summary"),
    path(
        "generate-bullet-points/",
        GenerateBulletPoints.as_view(),
        name="generate-bullet-points",
    ),
]
