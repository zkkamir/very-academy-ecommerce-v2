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
            "format: required, letters, numbers, underscores or hyphens,"
            " max-150"
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


class Product(models.Model):
    """
    Product details table.
    """

    web_id = models.CharField(
        _("product website ID"),
        max_length=50,
        unique=True,
        help_text=_("format: required, unique"),
    )
    slug = models.SlugField(
        _("product safe URL"),
        max_length=255,
        help_text=_(
            "format: required, letters, numbers, underscores or hyphens"
        ),
    )
    name = models.CharField(
        _("product name"),
        max_length=255,
        help_text=_("format: required, max-255"),
    )
    description = models.TextField(
        _("product description"), help_text=_("format: required")
    )
    category = TreeManyToManyField(Category)
    is_active = models.BooleanField(
        _("product visibility"),
        default=True,
        help_text=_("format: true=prodoct visibility"),
    )
    created_at = models.DateTimeField(
        _("date product was created"),
        auto_now_add=True,
        editable=False,
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        _("date product was updated"),
        auto_now=False,
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
    Product type table
    """

    name = models.CharField(
        _("type of product"),
        max_length=255,
        unique=True,
        help_text=_("format: required, unique, max-255"),
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
    Product brand table
    """

    name = models.CharField(
        _("brand name"),
        max_length=255,
        unique=True,
        help_text=_("format: required, unique, max-255"),
    )


class ProductAttribute(models.Model):
    """
    Product attribute table
    """

    name = models.CharField(
        _("product attribute name"),
        max_length=255,
        unique=True,
        help_text=_("format: required, unique, max-255"),
    )
    description = models.TextField(
        _("product attribute description"),
        help_text=_("format: required"),
    )

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """
    Product attribute value table
    """

    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name="product_attribute",
        on_delete=models.PROTECT,
    )
    attribute_value = models.CharField(
        _("attribute value"),
        max_length=255,
        help_text=_("format: required, max-255"),
    )

    def __str__(self):
        return f"{self.product_attribute.name} : {self.attribute_value}"


class ProductInventory(models.Model):
    """
    Product inventory table
    """

    sku = models.CharField(
        _("stock keeping unit"),
        max_length=20,
        unique=True,
        help_text=_("format: required, unique, max-20"),
    )
    upc = models.CharField(
        _("universal product code"),
        max_length=12,
        unique=True,
        help_text=_("format: required, unique, max-12"),
    )
    product_type = models.ForeignKey(
        ProductType, related_name="product_type", on_delete=models.PROTECT
    )
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.PROTECT
    )
    brand = models.ForeignKey(
        Brand, related_name="brand", on_delete=models.PROTECT
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name="product_attribute_values",
        through="ProductAttributeValues",
    )
    is_active = models.BooleanField(
        _("product visibility"),
        default=True,
        help_text=_("format: true=product visible"),
    )
    retail_price = models.DecimalField(
        _("recommended retail price"),
        max_digits=5,
        decimal_places=2,
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )
    store_price = models.DecimalField(
        _("regular store price"),
        max_digits=5,
        decimal_places=2,
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )
    sale_price = models.DecimalField(
        _("sale price"),
        max_digits=5,
        decimal_places=2,
        help_text=_("format: maximum price 999.99"),
        error_messages={
            "name": {
                "max_length": _("the price must be between 0 and 999.99."),
            },
        },
    )
    weight = models.FloatField(
        _("product weight"),
    )
    created_at = models.DateTimeField(
        _("date sub-product created"),
        auto_now_add=True,
        editable=False,
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        _("date sub-product updated"),
        auto_now=True,
        help_text=_("format: Y-m-d H:M:S"),
    )

    def __str__(self):
        return self.product.name


class Media(models.Model):
    """
    The product image table.
    """

    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.PROTECT,
        related_name="media_product_inventory",
    )
    image = models.ImageField(
        _("product image"),
        upload_to="images/",
        default="images/default.png",
        help_text=_("format: required, default-default.png"),
    )
    alt_text = models.CharField(
        _("alternative text"),
        max_length=255,
        help_text=_("format: required, max-255"),
    )
    is_feature = models.BooleanField(
        _("product default image"),
        default=False,
        help_text=_("format: default=false, true=default image"),
    )
    created_at = models.DateTimeField(
        _("product visibility"),
        auto_now_add=True,
        editable=False,
        help_text=_("format: Y-m-d H:M:S"),
    )
    updated_at = models.DateTimeField(
        _("date sub-product created"),
        auto_now=True,
        help_text=_("format: Y-m-d H:M:S"),
    )

    class Meta:
        verbose_name = _("product image")
        verbose_name_plural = _("product images")


class Stock(models.Model):
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name="product_inventory",
        on_delete=models.PROTECT,
    )
    last_checked = models.DateTimeField(
        _("inventory stock check date"),
        unique=False,
        null=True,
        blank=True,
        help_text=_("format: Y-m-d H:M:S, null-true, blank-true"),
    )
    units = models.IntegerField(
        _("units/qty of stock"),
        default=0,
        help_text=_("format: required, default-0"),
    )
    units_sold = models.IntegerField(
        _("units sold to date"),
        default=0,
        help_text=_("format: required, default-0"),
    )


class ProductAttributeValues(models.Model):
    """
    Product attribute values link table
    """

    attributevalues = models.ForeignKey(
        "ProductAttributeValue",
        related_name="attributevaluess",
        on_delete=models.PROTECT,
    )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name="productattributevaluess",
        on_delete=models.PROTECT,
    )

    class Meta:
        unique_together = (("attributevalues", "productinventory"),)
