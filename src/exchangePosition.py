from dataclasses import dataclass


@dataclass
class ExchangePosition():
    pair : str
    side : str
    contracts : int
    contractSize : float
    leverage : int

    @property
    def volume(self) -> float:
        return self.contracts * self.contractSize