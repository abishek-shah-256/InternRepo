
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/clearcache/', include('clearcache.urls')),
    path('admin/', admin.site.urls),
    path("__reload__/", include("django_browser_reload.urls")),
    path('accounts/', include('allauth.urls')),

    path('', include('app1.urls')),
    path('profile/', include('profiles.urls', namespace='profiles')),
    
    path("chat/", include("chat.urls")),
    
]

# FOR IMAGE HANDLING
urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT ) 
