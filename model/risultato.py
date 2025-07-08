import datetime
from dataclasses import dataclass


@dataclass
class Risultato:
    d : int
    t : datetime.time


