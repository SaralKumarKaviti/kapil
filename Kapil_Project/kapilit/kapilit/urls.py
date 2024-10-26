"""
URL configuration for kapilit project.

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
from django.contrib import admin
from django.urls import path
from counselor_app.views import counselor_login,manager_login,manager_dashboard_page,manager_logout,counselor_login,counselor_dashboard_page,counselor_logout,manager_logout,add_role

urlpatterns = [
    path('admin/', admin.site.urls),

    path('counselor-login',counselor_login,name="counselor_login"),
    path('counselor-dashboard-page',counselor_dashboard_page,name="counselor_dashboard_page"),
    path('counselor-logout',counselor_logout,name="counselor_logout"),

    path('manager-login',manager_login,name="manager_login"),
    path('manager-dashboard-page',manager_dashboard_page,name="manager_dashboard_page"),
    path('add-role',add_role,name='add_role'),
    path('manager-logout',manager_logout,name="manager_logout")
]