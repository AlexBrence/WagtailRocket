from django.utils.translation import gettext_lazy as _

from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from streams import blocks as custom_blocks


class HomePage(Page):
    template = 'home/home_page.html'
    max_count = 1

    class Meta:
        verbose_name = _("Home Page")
        verbose_name_plural = _("Home Pages")

    content = StreamField(
        [
            ('title_and_text', custom_blocks.TitleAndTextBlock()),
            ('full_rich_text', custom_blocks.RichTextBlock()),
            ('cards', custom_blocks.CardBlock()),
            ('carousel', custom_blocks.CarouselBlock()), 
            ('carousel_celebrity', custom_blocks.CarouselCelebrityBlock()),
            ('hozirontal_rule', custom_blocks.HorizontalRuleBlock()),
        ],
        null=True,
        blank=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel('content'),
    ]

    # TODO: figure out how it affects db; also here it might be ok to set few styles
    CONTAINER_BLOCKS = [
        "title_and_text", "full_rich_text", 
    ]

