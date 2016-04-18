from django.apps import AppConfig
from watson import search as watson


class AppConfig(AppConfig):
    name = 'app'

    def ready(self):
        # allow to use models in text search (django-watson)
        Partner = self.get_model("Partner")
        Product = self.get_model("Product")
        Article = self.get_model("Article")
        Category = self.get_model("Category")
        TopCategory = self.get_model('TopCategory')
        watson.register(Partner.objects.filter(is_hidden=False), fields=('title', 'desc',))
        watson.register(Product.objects.filter(is_hidden=False),
                        fields=('title_ru', 'desc_short_ru', 'desc_full_ru', 'specifications_ru', 'options_ru',
                                'mentions_ru',)
                        )
        watson.register(Article.objects.filter(is_hidden=False),
                        fields=('title_ru', 'text_ru', 'date', 'source_url', 'tags'),
                        store=('slug',)
                        )
        watson.register(Category.objects.filter(is_hidden=False), fields=('title_ru', 'parent_category',))
        watson.register(TopCategory.objects.filter(is_hidden=False), fields=('title_ru',))
