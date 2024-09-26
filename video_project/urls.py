from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import path, include
from django.contrib import admin

schema_view = get_schema_view(
    openapi.Info(
        title="Video Project API",
        default_version='v1',
        description="API documentation for the video project",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="shokoohrigi22@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=([permissions.AllowAny]),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('video.urls')),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
