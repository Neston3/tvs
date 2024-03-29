"""fyp1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, include

from FYP import settings
from tvs import views as view
from tvs.views import ProfileView, Pdf

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('', view.index, name='index'),
    path('home/', view.home, name='home'),
    path('home/apply/', view.apply, name='apply'),
    path('home/status', view.status_view, name='status'),
    path('home/profile', view.login_required(ProfileView.as_view()), name='profile'),
    path('admin/clean', view.approveVolunteer, name='clean'),
    path('signup/', view.UserFormView.as_view(), name='signup'),
    path('signup/complete', view.UserCompleteSignUp.as_view(), name='complete_signup'),
    path('accounts/', include('django.contrib.auth.urls'), name='login'),
    path('accounts/', include('django.contrib.auth.urls'), name='logout'),
    path('render/pdf/<str:full_name>', Pdf.as_view(), name='user_data'),
    path('manage/approve/<str:full_name>',view.updateStatus,name='approve'),
    path('manage/ed-level/<str:certificate>',view.manage_applicant,name='manage_applicant')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
