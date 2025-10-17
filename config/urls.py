
from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

# Swagger/OpenAPI Schema
schema_view = get_schema_view(
    openapi.Info(
        title="Task Manager API",
        default_version='v1',
        description="""
        A RESTful API for managing tasks with user authentication.
        
        ## Features
        - User registration and authentication (JWT)
        - CRUD operations for tasks
        - Task filtering and pagination
        - Role-based permissions
        
        ## Authentication
        This API uses JWT (JSON Web Tokens) for authentication.
        
        To authenticate:
        1. Register a new user at `/api/auth/register/`
        2. Login at `/api/auth/login/` to get access and refresh tokens
        3. Include the access token in the Authorization header: `Bearer <token>`
        
        ## Rate Limiting
        - Anonymous users: Limited endpoints
        - Authenticated users: Full access to task management
        """,
        terms_of_service="https://www.example.com/terms/",
        contact=openapi.Contact(email="contact@taskmanager.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    # Admin panel
    path('admin/', admin.site.urls),
    
    # API endpoints
    path('api/auth/', include('apps.authentication.urls')),
    path('api/tasks/', include('apps.tasks.urls')),
    
    # API Documentation
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('api/schema/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
]

# Customize admin site
admin.site.site_header = "Task Manager Administration"
admin.site.site_title = "Task Manager Admin Portal"
admin.site.index_title = "Welcome to Task Manager Admin"