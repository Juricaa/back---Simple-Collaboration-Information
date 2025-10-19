from django.urls import path, include
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Configuration de la documentation Swagger
schema_view = get_schema_view(
    openapi.Info(
        title="API Collaborations et Informations",
        default_version='v1',
        description="Documentation interactive de l'API C&I",
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="support@tour-op.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [ 

        path('api/regions/', include('regions.urls')),
        path('api/utilisateurs/', include('utilisateurs.urls')),
        path('api/entites/', include('entites.urls')),
        path('api/axes/', include('axes.urls')),
        path('api/objectifs/', include('objectifs.urls')),
        path('api/projets/', include('projets.urls')),
        path('api/entites-projets/', include('entitesprojets.urls')),
        path('api/rapports/', include('rapports.urls')),
        path('api/realisations/', include('realisations.urls')),
        path('api/commentaires/', include('commentaires.urls')), 
        path('api/notifications/', include('notifications.urls')),
       
        re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'), 
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'), 
        path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'), 
]
