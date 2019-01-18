"""coranno URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from django.contrib.auth.views import LoginView, PasswordResetView, LogoutView
from rest_framework import routers
from django.views.generic.base import RedirectView

from dataset.urls import router as dataset_router
from project.urls import router as project_router
router = routers.DefaultRouter()
router.registry.extend(dataset_router.registry)
router.registry.extend(project_router.registry)

urlpatterns = [
    path('', RedirectView.as_view(url='project', permanent=False), name='index'),

    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html',
                                     redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
    
    path('api/', include(router.urls)),
    path('dataset/', include('dataset.urls')),
    path('project/', include('project.urls')),
]