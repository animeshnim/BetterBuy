"""BetterBuy URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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



# Modules Import
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
import os



# Import from Apps
from . import views



# URL Patterns
urlpatterns = [
    # Primary URLs
    path('', views.Index, name = 'HomePage'),
    path('admin/', admin.site.urls),


    # Application URLs
    path('account/', include('Account.urls')),
    path('catalogue/', include('Catalogue.urls')),
    path('order/', include('Order.urls')),


    # Error Page URLs:
    # 4xx Errors:
    path('400', views.Error400, name = 'Error400'),
    path('403', views.Error403, name = 'Error403'),
    path('404', views.Error404, name = 'Error404'),

    # 5xx Errors:

]



# Error Pages URL's:
# 4xx Errors:
handler400 = 'BetterBuy.views.Error400'
handler403 = 'BetterBuy.views.Error403'
handler404 = 'BetterBuy.views.Error404'

# 5xx Errors:
# handler500 = 'MyStore.views.Error500'



# URL Pattern Settings for Debugging
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
