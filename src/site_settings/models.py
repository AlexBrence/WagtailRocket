from datetime import datetime

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

from wagtail.models import Orderable
from wagtail.admin.panels import FieldPanel, MultiFieldPanel, InlinePanel
from wagtail.contrib.settings.models import BaseSiteSetting, register_setting, BaseGenericSetting

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel


@register_setting
class SocialMedia(BaseSiteSetting):
    """ Social media settings """
    verbose_name = _("Social Media")

    X = models.URLField(blank=True, null=True, help_text=_("X (Twitter) URL"), max_length=500)
    facebook = models.URLField(blank=True, null=True, help_text=_("Facebook URL"), max_length=500)
    instagram = models.URLField(blank=True, null=True, help_text=_("Instagram URL"), max_length=500)
    youtube = models.URLField(blank=True, null=True, help_text=_("Youtube URL"), max_length=500)
    tiktok = models.URLField(blank=True, null=True, help_text=_("TikTok URL"), max_length=500)

    panels = [
        MultiFieldPanel([
            FieldPanel("X"),
            FieldPanel("facebook"),
            FieldPanel("instagram"),
            FieldPanel("youtube"),
            FieldPanel("tiktok"),
        ], heading=_("Social Media"))
    ]


class WorkDay(Orderable):
    verbose_name = _("Workday")

    class Days(models.TextChoices):
        MON = "Mon", _("Monday")
        TUE = "Tue", _("Tuesday")
        WED = "Wed", _("Wednesday")
        THU = "Thu", _("Thursday")
        FRI = "Fri", _("Friday")
        SAT = "Sat", _("Saturday")
        SUN = "Sun", _("Sunday")

    opening_hours = ParentalKey("OpeningHours", on_delete=models.CASCADE, related_name="workdays")
    day = models.CharField(_("Day"), max_length=3, choices=Days, null=True)
    is_closed = models.BooleanField(_("Is Closed"), default=False, null=True)
    from_hour = models.TimeField(_("From Hour"), null=True, blank=True)
    to_hour = models.TimeField(_("To Hour"), null=True, blank=True)
    from_hour2 = models.TimeField(_("From Hour 2"), null=True, blank=True, help_text=_("Set if reopens in the same day"))
    to_hour2 = models.TimeField(_("To Hour 2"), null=True, blank=True)

    panels = [
        MultiFieldPanel([
                FieldPanel("day"),
                FieldPanel("is_closed"),
                FieldPanel("from_hour"),
                FieldPanel("to_hour"),
                FieldPanel("from_hour2"),
                FieldPanel("to_hour2"),
            ]
        )
    ]


@register_setting
class OpeningHours(ClusterableModel, BaseGenericSetting):
    verbose_name = _("Opening Hours")

    panels = [
        InlinePanel("workdays", label=_("Workday"))
    ]


class Email(Orderable):
    contact = ParentalKey("Contact", on_delete=models.CASCADE, related_name="emails", null=True)
    email = models.EmailField("Email", null=True, blank=False)

    panels = [
        FieldPanel("email"),
    ]

    def __str__(self):
        return self.email


class PhoneNumber(Orderable):
    verbose_name = _("Phone Number")

    contact = ParentalKey("Contact", on_delete=models.CASCADE, related_name="phone_numbers", null=True)
    description = models.CharField(_("Owner"), max_length=50, null=True, blank=False)
    phone_number = models.CharField(_("Phone Number"), max_length=35, null=True, blank=False)

    panels = [
        MultiFieldPanel([
                FieldPanel("description"),
                FieldPanel("phone_number"),
            ]
        )
    ]

    def __str__(self):
        return f'{self.description}: {self.phone_number}'


class Location(Orderable):
    verbose_name = _("Location")

    contact = ParentalKey("Contact", on_delete=models.CASCADE, related_name="locations", null=False)
    street = models.CharField(_("Street and City"), max_length=128, null=False, blank=False)
    maps_url = models.URLField(_("Location URL"), null=False, blank=False, help_text=_("Google maps URL or similar"), max_length=1024)


@register_setting
class Contact(ClusterableModel, BaseSiteSetting):
    verbose_name = _("Contact")

    panels = [
        InlinePanel("phone_numbers", label=_("Phone Number")),
        InlinePanel("emails", label=_("Email")),
        InlinePanel("locations", label=_("Location")),
    ]


@register_setting
class Currency(BaseSiteSetting):
    verbose_name = _("Currency")

    unit = models.CharField(_("Unit"), max_length=32, help_text=_("Currency to use when showing prices (€, EUR, £, ...)"))

    panels = [
        FieldPanel("unit")
    ]


@register_setting
class CompanyInfo(BaseSiteSetting):
    verbose_name = _("Company Info")

    # TODO it should be possible to be null
    name = models.CharField(_("Name"), max_length=256)
    legal_entity_type = models.CharField(_("Legal Entity Type"), max_length=128)
    year_established = models.PositiveSmallIntegerField(_("Established in Year"), 
                                                        null=True, 
                                                        validators=[MaxValueValidator(limit_value=datetime.now().year)])
    show_copyright = models.BooleanField(_("Show Copyright in Footer"), default=False)

    panels = [
        MultiFieldPanel([
            FieldPanel("name"),
            FieldPanel("legal_entity_type"),
            FieldPanel("year_established"),
            FieldPanel("show_copyright"),
        ], heading=_("Company Info"))
    ]