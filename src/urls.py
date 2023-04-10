from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

admin.site.site_title = 'Administrator'
admin.site.site_header = 'XCalibur'
admin.site.index_title = 'Welcome back ...'

urlpatterns = [
    path('accounts/', include('authentication.urls')),
    path('', include('users.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
