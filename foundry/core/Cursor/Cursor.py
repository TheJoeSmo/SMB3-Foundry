from typing import Callable
import sqlite3
from functools import wraps

from foundry import default_database_path


class Connection:
    def __enter__(self):
        self.connection = sqlite3.connect(default_database_path)
        return self.connection

    def __exit__(self, type, value, traceback):
        self.connection.close()


class Cursor:
    # Reuse connection as it is very slow otherwise
    connection = sqlite3.connect(default_database_path)

    def __enter__(self):
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, type, value, traceback):
        self.connection.commit()
        self.cursor.close()


class Transaction:
    def __init__(self, connection: sqlite3.Connection):
        self.connection = connection
        self._inside_trasaction = False

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.connection.cursor()

    @property
    def inside_transaction(self) -> bool:
        return self._inside_trasaction

    def begin(self):
        if not self.inside_transaction:
            self.connection.execute("BEGIN TRANSACTION")
            self._inside_trasaction = True
        else:
            raise RuntimeError("Already inside a transaction")

    def commit(self):
        if not self.inside_transaction:
            raise RuntimeError("Not inside a transaction")
        else:
            self.connection.execute("COMMIT")
            self._inside_trasaction = False


def create_needed_trasactions():
    connection = sqlite3.connect(default_database_path)
    transaction = Transaction(connection)

    def request_to_be_inside_transaction(func: Callable):
        @wraps(func)
        def request_to_be_inside_transaction(*args, **kwargs):
            kwargs["transaction"] = transaction if transaction.inside_transaction else None
            return func(*args, **kwargs)

        return request_to_be_inside_transaction

    def require_a_transaction(func: Callable):
        @wraps(func)
        def require_a_transaction(*args, **kwargs):
            kwargs["transaction"] = transaction
            if transaction.inside_transaction:
                results = func(*args, **kwargs)
            else:
                transaction.begin()
                results = func(*args, **kwargs)
                transaction.commit()
            return results

        return require_a_transaction

    return request_to_be_inside_transaction, require_a_transaction


request_to_be_inside_transaction, require_a_transaction = create_needed_trasactions()
