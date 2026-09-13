import warnings

from django.db import models, connection
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.models import Page
from wagtail.search.query import Fuzzy
from wagtail.coreutils import resolve_model_string

from mixins.mixins import BreadcrumbMixin, HtmxMixin


class BasePage(Page):
    """ Common for all pages """
    template = None

    class Meta:
        abstract = True

    background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )

    def get_effective_background_image(self):
        """ Start from self and go up the tree until we find a non-empty one """
        page = self
        while page is not None:
            if hasattr(page.specific, "background_image") and page.specific.background_image:
                return page.specific.background_image
            page = page.get_parent()
        return None


class ListingPage(BreadcrumbMixin, HtmxMixin, BasePage):
    template = None 
    detail_page_model = None  # str expected in format "app_label.model_name"

    class Meta:
        abstract = True

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.detail_page_model is None:
            raise NotImplementedError("Child class has to set 'detail_page_model'!")

        self._detail_page_model = resolve_model_string(self.detail_page_model)

    def get_base_queryset(self):
        raise NotImplementedError("Child class has to override get_base_queryset method")

    def _set_child_listing_pages(self, request, context):
        """ Sets categories and subcategories """
        child_listing_pages = []
        subpage_listing_models = self.allowed_subpage_models() 

        if self._detail_page_model in subpage_listing_models:
            subpage_listing_models.remove(self._detail_page_model) 

        search_query = request.GET.get("q")
        for subpage_listing_model in subpage_listing_models:
            qs = subpage_listing_model \
                    .objects \
                    .live() \
                    .public() \
                    .child_of(self) \
                    .specific()

            if search_query:
                qs = self._apply_search(qs, search_query)

            child_listing_pages += qs

        context["child_listing_pages"] = child_listing_pages
        return context

    def _set_pagination(self, request, context, qs):
        ITEMS_PER_PAGE = 20
        PAGE_KWARG = "page_num"

        page_num = int(request.GET.get(PAGE_KWARG, 1))

        paginator = Paginator(qs, ITEMS_PER_PAGE)
        num_pages = paginator.num_pages
        
        # Check if page number is valid
        try:
            objects = paginator.page(page_num)
        except PageNotAnInteger:
            objects = paginator.page(1)
        except EmptyPage:
            objects = paginator.page(num_pages)

        # Make dynamic paginator
        if num_pages <= 7 or page_num <= 4:  
            pages = [x for x in range(1, min(num_pages + 1, 7))]
        elif page_num > num_pages - 4:
            pages = [x for x in range(num_pages - 4, num_pages + 1)]
        else:
            pages = [x for x in range(page_num - 2, page_num + 3)]

        context.update({
            "objects": objects,
            "pages": pages
        })
        return qs

    def _set_ordering(self, request, qs):
        ORDERING_DICT = {
            'price': 'price',
            'price-desc': '-price',
            'date': 'first_published_at',
            'date-desc': '-first_published_at',
        }
        DEFAULT_ORDERING = "date-desc"
        ORDER_KWARG = "order"

        # If we have a search query leave ordering to Wagtail
        if request.GET.get("q"):
            return qs

        ordering = request.GET.get(ORDER_KWARG, DEFAULT_ORDERING)

        order = ORDERING_DICT.get(ordering)
        qs = qs.order_by(order)
        return qs

    def _apply_search(self, qs, search_query):
        """ Applies search query and returns modified queryset """
        if not search_query:
            return qs

        if connection.vendor == "postgresql": # PostgreSQL specific
            qs = qs.filter(title__unaccent__trigram_word_similar=search_query) # TODO: test with Fuzzy, postgres support is valid now
        else:
            if settings.DEBUG is False:
                warnings.warn(
                    "SQLite search backend is being used. "
                    "Search quality is limited compared to PostgreSQL.",
                    UserWarning,
                    stacklevel=2
                )

            qs = qs.autocomplete(search_query)

        return qs

    def get_queryset(self, request, context):
        qs = self.get_base_queryset()

        # Check for search query, search by titles
        if search_query := request.GET.get("q", "").strip():
            qs = self._apply_search(qs, search_query)
            context["search_query"] = search_query
        return qs

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)

        qs = self.get_queryset(request, context)
        qs = self._set_ordering(request, qs)
        qs = self._set_pagination(request, context, qs)
        self._set_child_listing_pages(request, context)

        context.update({
            "background_image": self.get_effective_background_image()
        })
        return context
    

class CategoryListingPage(ListingPage):
    template = None

    class Meta:
        abstract = True


class SubcategoryListingPage(ListingPage):
    template = None

    class Meta:
        abstract = True


class DetailPage(BreadcrumbMixin, BasePage):
    template = None 

    class Meta:
        abstract = True