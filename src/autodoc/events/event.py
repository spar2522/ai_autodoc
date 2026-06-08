from dataclasses import asdict
from dataclasses import dataclass


@dataclass
class Event:

    type: str

    def to_dict(self):

        return asdict(self)
