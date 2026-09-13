import random

from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.models import Page, Orderable
from wagtail.admin.panels import FieldPanel
from wagtail.admin.panels import InlinePanel
from wagtail.fields import RichTextField
from modelcluster.fields import ParentalKey

from listing_pages_common.models import DetailPage, ListingPage, CategoryListingPage, SubcategoryListingPage


class ProductListingPage(ListingPage):
    template = "products/product_listing_page.html"
    partials_template = "products/partials/_products.html"
    max_count = 1

    parent_page_types = ["home.HomePage"]
    subpage_types = ["ProductCategoryListingPage"]
    detail_page_model = "products.ProductDetailPage"
    
    verbose_name = _("Product Listing Page")
    verbose_name_plural = _("Product Listing Pages")

    content_panels = Page.content_panels + [
        FieldPanel("background_image"),
    ]

    def __str__(self):
        return self.title

    def get_base_queryset(self):
        return ProductDetailPage.objects.live().public().prefetch_related("thumbnail_image")


class ProductCategoryListingPage(CategoryListingPage):
    template = "products/product_listing_page.html"
    partials_template = "products/partials/_products.html"

    parent_page_types = ["ProductListingPage"]
    subpage_types = ["ProductSubcategoryListingPage", "ProductDetailPage"]
    detail_page_model = "products.ProductDetailPage"

    def get_base_queryset(self):
        return ProductDetailPage.objects.live().public().descendant_of(self).prefetch_related("thumbnail_image")


class ProductSubcategoryListingPage(SubcategoryListingPage):
    template = "products/product_listing_page.html"
    partials_template = "products/partials/_products.html"

    parent_page_types = ["ProductCategoryListingPage"]
    subpage_types = ["ProductDetailPage"]
    detail_page_model = "products.ProductDetailPage"

    description = RichTextField(blank=True)

    def get_base_queryset(self):
        return ProductDetailPage.objects.live().public().descendant_of(self).prefetch_related("thumbnail_image")


class ProductDetailPage(DetailPage):
    template = 'products/product_detail_page.html'

    parent_page_types = ["ProductCategoryListingPage", "ProductSubcategoryListingPage"]
    subpage_types = []

    verbose_name = _("Product Detail Page")
    verbose_name_plural = _("Product Detail Pages")

    class Genders(models.TextChoices):
        MEN = "men", _("Men")
        WOMEN = "women", _("Women")
        UNISEX = "unisex", _("Unisex")

    description = RichTextField(blank=True)
    gender = models.CharField(_("Gender"), max_length=6, choices=Genders, null=True, blank=True)
    price = models.DecimalField(blank=True, decimal_places=2, max_digits=8)
    thumbnail_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=False,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

    content_panels = Page.content_panels + [
        FieldPanel('thumbnail_image'),
        InlinePanel('product_images', label=_("Product Images")),
        FieldPanel('description'),
        FieldPanel('gender'),
        FieldPanel('price'),
    ]

    def __str__(self):
        return self.title

    def _add_random_products(self):
        objects = ProductDetailPage.objects.live().public()
        objects_num = objects.count()
        
        if objects_num <= 3:
            random_products = list(objects)
        else:
            random_products = random.sample(list(objects), 3)

        return random_products

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context.update({
            "background_image": self.get_effective_background_image(),
            "random_products": self._add_random_products()
        })
        return context

    def save(self, *args, **kwargs):
        self.seo_title = self.title
        self.search_description = self.description
        super(ProductDetailPage, self).save(*args, **kwargs)


class ProductDetailImages(Orderable):
    product = ParentalKey(
        ProductDetailPage, 
        on_delete=models.CASCADE, 
        related_name='product_images',
    )
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.CASCADE,
        related_name='+',
        null=True,
        blank=True
    )

    panels = [
        FieldPanel('image')
    ]

