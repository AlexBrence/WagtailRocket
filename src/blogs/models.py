import random 

from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.fields import StreamField
from wagtail.models import Page
from wagtail.admin.panels import FieldPanel

from streams import blocks
from listing_pages_common.models import DetailPage, ListingPage, CategoryListingPage


class BlogListingPage(ListingPage):
    template = "blogs/blog_listing_page.html"
    partials_template = "blogs/partials/_posts.html"
    max_count = 1

    parent_page_types = ["home.HomePage"]
    subpage_types = ["BlogDetailPage", "BlogCategoryListingPage"]
    detail_page_model = "blogs.BlogDetailPage"

    content_panels = Page.content_panels + [
        FieldPanel("background_image"),
    ]

    def get_base_queryset(self):
        return BlogDetailPage.objects.live().public().prefetch_related("thumbnail_image").specific().order_by("-first_published_at")


class BlogCategoryListingPage(CategoryListingPage):
    template = "blogs/blog_listing_page.html"
    partials_template = "blogs/partials/_posts.html"

    parent_page_types = ["BlogListingPage"]
    subpage_types = ["BlogDetailPage"]
    detail_page_model = "blogs.BlogDetailPage"

    def get_base_queryset(self):
        return BlogDetailPage.objects.live().public().descendant_of(self).prefetch_related("thumbnail_image")


class BlogDetailPage(DetailPage):
    template = "blogs/blog_detail_page.html"
    parent_page_types = ["BlogListingPage", "BlogCategoryListingPage"]
    subpage_types = []

    thumbnail_image = models.ForeignKey(
        "wagtailimages.Image",
        blank=False,
        null=True,
        related_name="+",
        on_delete=models.SET_NULL
    )
    
    content = StreamField(
        [
            ("full_rich_text", blocks.RichTextBlock()),
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("thumbnail_image"),
        FieldPanel("content"),
    ]

    def _add_random_posts(self):
        objects = BlogDetailPage.objects.live().public()
        objects_num = objects.count()
        
        if objects_num <= 3:
            random_posts = list(objects)
        else:
            random_posts = random.sample(list(objects), 3)

        return random_posts

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({
            "background_image": self.get_effective_background_image(),
            "random_posts": self._add_random_posts()
        })
        return context
