from django.db import models
from django.utils.translation import gettext_lazy as _

from wagtail.admin.panels import FieldPanel
from wagtail.fields import StreamField
from wagtail.models import Page

from streams import blocks


class FlexPage(Page):
    ''' Flexible page class '''
    template = 'flex/flex_page.html'

    class Meta:
        verbose_name = _("Flex Page")
        verbose_name_plural = _("Flex Pages")

    background_image = models.ForeignKey(
        'wagtailimages.Image',
        blank=True,
        null=True,
        related_name='+',
        on_delete=models.SET_NULL
    )
    subtitle = models.CharField(max_length=100, null=True, blank=True)
    content = StreamField(
        [
            ('title_and_text', blocks.TitleAndTextBlock()),
            ('full_rich_text', blocks.RichTextBlock()),
            ('cards', blocks.CardBlock()),
            ('slides', blocks.CarouselBlock()),
            ('hozirontal_rule', blocks.HorizontalRuleBlock()),
            ('carousel_celebrity', blocks.CarouselCelebrityBlock()),
            ('carousel', blocks.CarouselBlock()),
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel('background_image'),
        FieldPanel('subtitle'),
        FieldPanel('content'),
    ]
