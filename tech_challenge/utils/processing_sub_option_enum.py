from enum import Enum
from typing import Optional

class ProcessingSubOption(str, Enum):
    VINIFERA = "01"
    AMERICAN_HYBRID = "02"
    TABLE_GRAPE = "03"
    UNCLASSIFIED = "04"
    
    def __str__(self):
        return self.name
    
    @classmethod
    def from_name(cls, name: str) -> Optional['ProcessingSubOption']:
        try:
            return cls[name.upper()]
        except KeyError:
            return None