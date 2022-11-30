from django.conf.urls import url
from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
   openapi.Info(
      title="TakeHome API documentation",
      default_version='v1.0.0',
      description="Documentation of the API TakeHome",
      contact=openapi.Contact(email="jf.huete@gmail.com"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('', include(('movies.urls', 'movies'))),
    path('', include(('actors.urls', 'actors'))),
    url(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'
    ),
    url(
        r'^redoc/$',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'
    ),
    path('admin/', admin.site.urls),
]
