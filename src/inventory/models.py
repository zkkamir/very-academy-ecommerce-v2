from operator import mod
from django.db import models
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Category(MPTTModel):
    """
    Inventory Category table implemented with MPTT.
    """

    name = models.CharField(
        _("category name"),
        max_length=100,
        help_text=_("format: required, max-100"),
    )
    slug = models.SlugField(
        _("category safe url"),
        max_length=150,
        help_text=_(
            "format: required, letters, numbers, underscores or hyphens, max-150"
        ),
    )
    is_active = models.BooleanField(_("is active"), default=True)

    parent = TreeForeignKey(
        "self",
        on_delete=models.PROTECT,
        related_name="children",
        null=True,
        blank=True,
        verbose_name=_("parent of category"),
        help_text=_("format: not required"),
    )

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        verbose_name = _("product category")
        verbose_name_plural = _("product categories")

    def __str__(self):
        return self.name
