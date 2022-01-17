from tty import CFLAG
import factory
import pytest
from faker import Faker
from pytest_factoryboy import register

fake = Faker()

from inventory import models


class CategoryFactory(factory.django.DjangoModelFactory):
    """A factory for category model."""

    class Meta:
        model = models.Category

    name = factory.Sequence(lambda x: f"cat_slug_{x}")
    slug = fake.lexify(text="cat_slug_??????")


register(CategoryFactory)


class ProductFactory(factory.django.DjangoModelFactory):
    """A factory for product model."""

    class Meta:
        model = models.Product

    web_id = factory.Sequence(lambda x: f"web_id_{x}")
    slug = fake.lexify(text="prod_slug_??????")
    name = fake.lexify(text="prod_name_??????")
    description = fake.text()
    is_active = True
    created_at = "2022-01-17 12:57:42.259283"
    updated_at = "2022-01-17 12:57:42.259283"

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            return

        if extracted:
            for cat in extracted:
                self.category.add(cat)


register(ProductFactory)
