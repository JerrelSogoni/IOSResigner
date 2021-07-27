from __future__ import annotations

from abc import abstractmethod


class AbstractValidator:
    def __init__(self):
        pass

    @property
    @abstractmethod
    def validate(self, result) -> bool:
        pass
