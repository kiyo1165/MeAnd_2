from django.contrib import admin
from django.urls import path, include
from django.contrib.staticfiles.urls import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('plan/', include('plan.urls')),
    path('accounts/', include('allauth.urls')),
    path('', include( 'accounts.urls' ) ),
    path('message/', include('message.urls')),
    path('comment/', include('usercomments.urls')),
    path('reserve/', include('reservation.urls')),
    path('', include('follow.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)