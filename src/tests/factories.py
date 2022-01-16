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
