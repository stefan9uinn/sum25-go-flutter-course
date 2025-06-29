from django.core.management import call_command
from django.test import TransactionTestCase

class MigrationsTest(TransactionTestCase):
    databases = {'default'}

    def test_apply_migrations(self):
        """
        Проверяем, что все миграции применяются без ошибок на чистой БД.
        """
        # Пробуем выполнить migrate на тестовой базе
        call_command("migrate", verbosity=0, interactive=False)

