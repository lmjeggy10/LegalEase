"""Law_and_Order URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path

from law.views import IndexView, LoginView,LawRegs,UserRegister, Forgot_Password
from law import admin_urls,law_urls,user_urls
from Law_and_Order import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', IndexView.as_view()),
    path('login', LoginView.as_view()),
    path('LawRegs', LawRegs.as_view()),
    path('UserRegister', UserRegister.as_view()),
    path('admin/', admin_urls.urls()),
    path('law/', law_urls.urls()),
    path('user/', user_urls.urls()),
    path('forgot_pass',Forgot_Password.as_view())

]

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)