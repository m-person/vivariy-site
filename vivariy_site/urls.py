# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
# from django.conf.urls.i18n import i18n_patterns
from app.views import (MainView, CatalogView, CategoryView, ProductView, ManufacturersView, ArticleListView,
                       ArticleDetailView, ContactsView,)

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^catalog/$', CatalogView.as_view(), name='catalog'),
    url(r'^catalog/(?P<slug>[-_\w]*)$', CategoryView.as_view(), name='category'),
    url(r'^products/(?P<slug>[-_\w]*)$', ProductView.as_view(), name='product'),
    url(r'^partners/$', ManufacturersView.as_view(), name='manufacturers'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^articles/$', ArticleListView.as_view(), name='article_list'),
    url(r'^articles/(?P<slug>[-_\w]*)$', ArticleDetailView.as_view(), name='article_details'),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
]

# access to uploaded files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
