from django.contrib import admin
from django.urls import path, include  # ✅ Corrección

urlpatterns = [
    path('admin/', admin.site.urls),
    path('core/', include('core.urls')), 
]