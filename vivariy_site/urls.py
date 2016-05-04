# coding=utf-8
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from app import sitemaps
from app.views import (MainView, CatalogView, CategoryView, ProductView, PartnersView, ArticleListView,
                       ArticleDetailView, ContactsView, RequestSuccess, cart_count_request, media_backup_request,
                       LangRedirect, SubscribeView, get_subscribers, )

sitemaps = {
    'staticpages': sitemaps.StaticViewsMap,
    'catalog': sitemaps.CatalogSitemap,
    'products': sitemaps.ProductsSitemap,
    'articles': sitemaps.ArticlesSitemap
}

urlpatterns = [
    url(r'^admin/', include('smuggler.urls')),
    url(r'^admin/mediabackup/', media_backup_request, ),
    url(r'^admin/get_subscribers/', get_subscribers),
    url(r'^admin/', admin.site.urls),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    url(r'^$', MainView.as_view(), name='main'),
    url(r'^catalog/$', CatalogView.as_view(), name='catalog'),
    url(r'^catalog/(?P<slug>[-_\w]*)$', CategoryView.as_view(), name='category'),
    url(r'^products/(?P<slug>[-_\w]*)$', ProductView.as_view(), name='product'),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^lang_redirect', LangRedirect.as_view(), name='lang_redirect'),
    url(r'^articles/$', ArticleListView.as_view(), name='article_list'),
    url(r'^articles/(?P<slug>[-_\w]*)$', ArticleDetailView.as_view(), name='article_details'),
    url(r'^contacts/$', ContactsView.as_view(), name='contacts'),
    url(r'^tagging_autocomplete/', include('tagging_autocomplete.urls')),
    url(r'^request_success/', RequestSuccess.as_view(), name='request_success'),
    url(r'^xhr/cart_count/', cart_count_request),
    url(r"^search/", include("watson.urls", namespace="watson")),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    url(r'^robots\.txt$', include('robots.urls')),
    url(r'^subscribe/', SubscribeView.as_view(), name='subscribe'),
]

# access to uploaded files
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# internationalization some pages
urlpatterns += i18n_patterns(
    url(r'^partners/$', PartnersView.as_view(), name='partners'),
)
