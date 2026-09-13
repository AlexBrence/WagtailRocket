from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    ''' Just a plain title and a text '''
    title = blocks.CharBlock(required=True, max_length=100)
    text = blocks.TextBlock(required=True)

    class Meta:
        template = 'streams/title_and_text_block.html'
        icon = 'edit'
        label = 'Title & Text'


class HorizontalRuleBlock(blocks.StructBlock):
    ''' Just a <hr> tag '''
    class Meta:
        template = None
        icon = 'edit'
        label = 'Horizontal Rule'

    def render(self, value, context=None):
        return format_html('<hr>')


class RichTextBlock(blocks.RichTextBlock):
    ''' Text with styling options '''
    class Meta:
        template = 'streams/rich_text_block.html'
        icon = 'edit'
        label = 'Styled Text'


class CardBlock(blocks.StructBlock):
    ''' Cards with image, text and buttons '''
    title = blocks.CharBlock(required=True)
    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=True)),
                ('title', blocks.CharBlock(required=True, max_length=40)),
                ('text', blocks.TextBlock(required=True, max_length=4096)),
                ('button_page', blocks.PageChooserBlock(required=False, help_text=_("Link to a page on your website"))), 
                ('button_url', blocks.URLBlock(required=False, help_text=_("URL to external website"))), # TODO is this good enough?
            ],
        )
    )

    class Meta:
        template = 'streams/card_block.html'
        icon = 'placeholder'
        label = 'Promotion Cards'


class CarouselBlock(blocks.StructBlock):
    ''' Carousel with image, title and description (for news)'''
    slides = blocks.ListBlock(
        blocks.StructBlock(
            [
                ('image', ImageChooserBlock(required=True)),
                ('title', blocks.CharBlock(required=False, max_length=50)),
                ('description', blocks.TextBlock(required=False, max_length=200)),
                ('page_chooser', blocks.PageChooserBlock(required=False)),
            ],
        )
    )

    class Meta:
        template = 'streams/carousel_block.html'
        icon = 'edit'
        label = 'Carousel'


class CarouselCelebrityBlock(CarouselBlock):
    title = blocks.CharBlock(required=False)

    class Meta:
        template = 'streams/carousel_celebrity_block.html'
        icon = 'edit'
        label = 'Carousel Celebrities'



