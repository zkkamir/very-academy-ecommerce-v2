import pytest


@pytest.fixture
def create_admin_user(django_user_model):
    """Create and return an admin user."""
    user = django_user_model.objects.create_superuser(
        username="admin", password="admin123"
    )
    return user
