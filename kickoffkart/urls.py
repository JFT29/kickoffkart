<<<<<<< HEAD
﻿from django.urls import path, include

urlpatterns = [
    path("", include("main.urls")),
]
=======
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
>>>>>>> d8c3a27bade94cfc77382312121f9bcee581f472
