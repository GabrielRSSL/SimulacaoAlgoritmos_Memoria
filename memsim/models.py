"""Intervalos semiabertos e solicitações imutáveis."""

from dataclasses import dataclass
from typing import NamedTuple


class Block(NamedTuple):
    start: int
    size: int

    @property
    def end(self):
        return self.start + self.size


@dataclass(frozen=True, slots=True)
class Request:
    id: int
    arrival: int
    size: int
    duration: int

    def __post_init__(self):
        if any(type(x) is not int for x in (self.id, self.arrival, self.size, self.duration)):
            raise ValueError("Os campos da solicitação devem ser inteiros.")
        if self.id <= 0 or self.arrival < 0 or self.size <= 0 or self.duration <= 0:
            raise ValueError("ID, tamanho e permanência positivos; chegada não negativa.")
