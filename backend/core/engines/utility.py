import psycopg2

from core.engines.exceptions import DBExists, DBNotExists


def postgres_wrap_exceptions(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except psycopg2.errors.DuplicateDatabase:
            raise DBExists

        except psycopg2.OperationalError as e:
            if "does not exist" in str(e):
                raise DBNotExists
            raise e

    return wrapper

