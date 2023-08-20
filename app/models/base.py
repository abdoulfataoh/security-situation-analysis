# coding: utf-8

from abc import ABC, abstractmethod
from typing import Any


class ModelBase(ABC):

    @abstractmethod
    def predict(self, input_text: str) -> Any:
        pass
