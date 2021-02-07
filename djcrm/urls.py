"""djcrm URL Configuration

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
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.views import LoginView,LogoutView
#from leads.views import home_page
from leads.views import second_page,landing_page,Landingpageview,SignupView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Landingpageview.as_view(),name='landing-page'),
    path('leads/',include('leads.urls',namespace="leads")),
    path('agents/',include('agents.urls',namespace="agents")),

    #path('',home_page),
    path('signup/',SignupView.as_view(),name='signup'),
    path('second_page',second_page),
    path('login/',LoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(),name='logout')
]

if settings.DEBUG:
    urlpatterns+=static(settings.STATIC_URL,document_root=settings.STATIC_ROOT)