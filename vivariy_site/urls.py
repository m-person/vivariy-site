"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns
from app.views import (MainView, CatalogView, CategoryView, ProductView, ManufacturersView,)


urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^catalog/$', CatalogView.as_view(), name='catalog'),
    url(r'^catalog/(?P<slug>[-_\w]*)$', CategoryView.as_view(), name='category'),
    url(r'^products/(?P<slug>[-_\w]*)$', ProductView.as_view(), name='product'),
    url(r'^partners/$', ManufacturersView.as_view(), name='manufacturers'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
]

# access to uploaded files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
