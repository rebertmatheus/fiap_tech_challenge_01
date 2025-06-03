from enum import Enum
from typing import Optional

class SubOption(str, Enum):
    TABLE_WINE = "01"  # VINHO_MESA
    SPARKLING_WINE = "02"  # ESPUMANTES
    FRESH_GRAPES = "03"  # UVAS_FRESCAS
    RAISINS = "04"  # UVAS_PASSAS
    GRAPE_JUICE = "05"  # SUCO_UVA
    
    def __str__(self):
        return self.name
    
    @classmethod
    def from_name(cls, name: str) -> Optional['SubOption']:
        try:
            return cls[name.upper()]
        except KeyError:
            return None