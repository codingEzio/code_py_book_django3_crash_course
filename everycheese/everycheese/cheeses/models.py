from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from autoslug.fields import AutoSlugField
from model_utils.models import TimeStampedModel
from django_countries.fields import CountryField


class Cheese(TimeStampedModel):
    """
    Both of the third-party libraries were used to simplify the common jobs.
    """

    class Firmness(models.TextChoices):
        UNSPECIFIED = "unspecified", _("Unspecified")
        SOFT = "soft", _("Soft")
        SEMI_SOFT = "semi-soft", _("Semi-Soft")
        SEMI_HARD = "semi-hard", _("Semi-Hard")
        HARD = "hard", _("Hard")

    name = models.CharField(_("Name of cheese"), max_length=255)
    slug = AutoSlugField(
        _("Cheese Address"),
        unique=True,
        always_update=False,
        populate_from="name",
    )
    description = models.TextField(_("Description"), blank=True)
    firmness = models.CharField(
        _("Firmness"),
        max_length=20,
        choices=Firmness.choices,
        default=Firmness.UNSPECIFIED,
    )

    country_of_origin = CountryField("Country of Origin", blank=True)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("cheeses:detail", kwargs={"slug": self.slug})
