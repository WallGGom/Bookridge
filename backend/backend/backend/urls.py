"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_jwt.views import obtain_jwt_token, verify_jwt_token, refresh_jwt_token
from django.conf import settings
from django.conf.urls.static import static
# drf_yasg setting
from rest_framework import routers, permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# swagger 정보 설정, 관련 엔드포인트 추가
# swagger 엔드포인트는 DEBUG Mode에서만 노출
schema_view = get_schema_view(
    openapi.Info(
        title="BOOKRIDGE",
        default_version="v1",
        description="Test",
        terms_of_service="https://www.google.com/policies/terms/",
        # contact=openapi.Contact(email="test@test.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

if settings.DEBUG:
    urlpatterns = [
    path('admin/', admin.site.urls),
    # swagger
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/accounts/', include('accounts.urls')),
    path('api/token/', obtain_jwt_token),
    path('api/token/verify/', verify_jwt_token),
    path('api/token/refresh/', refresh_jwt_token),
    # path('api-auth/', include('rest_framework.urls')),
    path('api/books/', include('books.urls')),
    path('api/reviews/', include('reviews.urls')),
    path('api/libraries/', include('libraries.urls')),
    path('api/analyze/', include('analyze.urls'))
    # path('api/libraries/', include('libraries.urls')),
]
else:
    urlpatterns = [
        path('admin/', admin.site.urls),
        path('api/accounts/', include('accounts.urls')),
        path('api/token/', obtain_jwt_token),
        path('api/token/verify/', verify_jwt_token),
        path('api/token/refresh/', refresh_jwt_token),
        # path('api-auth/', include('rest_framework.urls')),
        path('api/books/', include('books.urls')),
        path('api/reviews/', include('reviews.urls')),
        path('api/libraries/', include('libraries.urls')),
        path('api/analyze/', include('analyze.urls'))
        # path('api/libraries/', include('libraries.urls')),
    ]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)