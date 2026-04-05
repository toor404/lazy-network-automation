from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('logout/', views.LogoutUser, name="logout"),
    path('login/', views.LoginPage, name="login"),
    path('register/', views.RegistrationPage, name="register"),
    path('', views.index, name='home'),
    path('admin/', admin.site.urls),
    path('masterdata/', include('masterdata.urls')),
    path('automation/', include('automation.urls')),
    path('nms/', include('nms.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)