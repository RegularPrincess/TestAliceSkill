"""TestAlice URL Configuration

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
from django.urls import path
import TestAlice.AliceSkillApp.view as alice_view
import TestAlice.WebInterfaceApp.view as interface_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', alice_view.alice_handler, name='alice_handler'),
    path('history/', interface_view.get_history, name='get_history'),
    path('accounts/login/', interface_view.login_user, name='login'),
]
