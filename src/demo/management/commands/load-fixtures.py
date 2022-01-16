from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """A command to make migrations, migrate them and
    load all the needed fixtures for testing."""

    def handle(self, *args, **options):
        call_command("makemigrations")
        call_command("migrate")
        call_command("loaddata", "db_admin_fixture.json")
        call_command("loaddata", "db_category_fixture.json")