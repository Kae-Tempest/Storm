"""
URL configuration for storm_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from ninja import NinjaAPI

from apps.authentication.api import router as auth_router
from apps.comments.api import router as comments_router
from apps.posts.api import router as posts_router
from apps.users.api import router as users_router
from core import settings

# Création de l'API principale

api = NinjaAPI()

# Ajout des routeurs avec leurs préfixes
api.add_router("/auth/", auth_router)
api.add_router("/users/", users_router)
api.add_router("/posts/", posts_router)
api.add_router("/comments/", comments_router)

urlpatterns = [path("admin/", admin.site.urls), path("api/", api.urls)]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
