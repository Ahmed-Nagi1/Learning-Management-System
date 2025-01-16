# ruff: noqa
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include
from django.urls import path, re_path
from django.views import defaults as default_views
from django.views.generic import TemplateView
from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularSwaggerView
from rest_framework.authtoken.views import obtain_auth_token
from lms.accounts.views import *

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

class SetCookieExampleView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        # الحصول على قيمة 'target' من البيانات المرسلة مع الطلب
        target = request.META.get('HTTP_ORIGIN', 'No origin provided') # افتراض قيمة افتراضية

        # طباعة 'target' في وحدة التحكم
        print(f"Target received: {target}")

        # إعداد الاستجابة
        response = Response({
            "message": "Cookie set successfully!",
            "target": target,  # إضافة 'target' إلى الاستجابة كإخراج اختباري
        })

        # إعداد الكوكي بدون أمان (HTTP فقط)
        response.set_cookie(
            key='my_cookie_name',          # اسم الكوكي
            value='my_cookie_value',       # قيمة الكوكي
            max_age=3600,                  # وقت انتهاء الصلاحية بالثواني
            httponly=False,                # يمكن الوصول للكوكي من JavaScript
            samesite=None,                 # السماح باستخدام الكوكي عبر المواقع (Cross-Site)
        )

        return response



urlpatterns = [
    path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("ex/", SetCookieExampleView.as_view(), name="ex"),
    # path("users/", include("lms.users.urls", namespace="users")),
    path("accounts/", include("allauth.urls")),
    path("auth/", include("allauth.headless.urls")),
    # Your stuff: custom urls includes go here
    # ...
    # Media files
    *static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT),
]
if settings.DEBUG:
    # Static file serving when using Gunicorn + Uvicorn for local web socket development
    urlpatterns += staticfiles_urlpatterns()

# API URLS
urlpatterns += [

    # path('authw/', include('dj_rest_auth.urls')),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    # path('auth/', include('lms.accounts.urls')),

    # path('app/', include('lms.app.urls')),


    # API base url
    # path("api/", include("config.api_router")),
    # DRF auth token
    path("api/auth-token/", obtain_auth_token),
    path("api/schema/", SpectacularAPIView.as_view(), name="api-schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="api-schema"),
        name="api-docs",
    ),
]

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
