# Edit file sistem_seminar/urls.py

from django.conf import settings
from django.urls import include, path
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail import urls as wagtail_urls

from search import views as search_views

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('admin/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('search/', search_views.search, name='search'),
    
    # Tambahkan URL untuk registrasi seminar dengan prefix 'register'
    path('register/', include('seminar.urls')),
    
    # For anything not caught by the above, fall back to Wagtail's page serving mechanism
    path('', include(wagtail_urls)),
]