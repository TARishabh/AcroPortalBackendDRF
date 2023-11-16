"""
URL configuration for acroportal project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path,include
from models_app.views import (
    getuser,
    registeruser,
    login,
    mark_attendance,
    view_attendance,
)
# from models_app.views import AttendanceViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path('getuser/',getuser),
    path('registeruser/',registeruser),
    path('login/',login),
    path('mark_attendance/',mark_attendance),
    path('view_attendance/',view_attendance),
    # path('test/',AttendanceViewSet.as_view({'post':'create'}))
]
