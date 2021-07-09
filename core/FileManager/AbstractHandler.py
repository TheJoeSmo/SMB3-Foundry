from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class AbstractHandler(ABC):
    @abstractmethod
    def generate(self, session: Session, **kwargs) -> None:
        """Generate a portion of a file to the database"""
