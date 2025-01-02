from django.conf import settings
from django.urls import path, re_path, include, reverse_lazy
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic.base import RedirectView
from rest_framework.authtoken import views


urlpatterns = [
    re_path(r"^auth/registration/account-confirm-email/(?P<key>[-:\w]+)/$", CustomConfirmEmailView.as_view(),name="account_confirm_email",),
    path('auth/registration/', include('dj_rest_auth.registration.urls')),
    path('auth/', include('dj_rest_auth.urls')),

    path('admin/', admin.site.urls),
    path('api-token-auth/', views.obtain_auth_token),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    re_path(r'^$', RedirectView.as_view(url=reverse_lazy('api-root'), permanent=False)),
     path('app/', include('LMS.app.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
