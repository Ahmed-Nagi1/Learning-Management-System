from django.urls import path, re_path, include
from dj_rest_auth.views import PasswordResetConfirmView
from . import views


urlpatterns = [
    path('', include('dj_rest_auth.urls')),
    path('registration/', include('dj_rest_auth.registration.urls')),
    path("registration/account-confirm-email/", views.ConfirmEmailAPIView.as_view(),name="account_confirm_email",),
    path(
        'password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm',
    ),
    path('change-email/', views.ChangeEmailView.as_view(), name='change_email'),
    path('user-info/', views.UserView.as_view()),
]
