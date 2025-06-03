from enum import Enum
from typing import Optional

class Segment(str, Enum):
    PRODUCTION = "02"
    PROCESSING = "03"
    SALES = "04"
    IMPORTATION = "05"
    EXPORTATION = "06"
    
    def __str__(self):
        return self.name
    
    @classmethod
    def from_name(cls, name: str) -> Optional['Segment']:
        try:
            return cls[name.upper()]
        except KeyError:
            return None