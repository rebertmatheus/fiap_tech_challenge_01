import re
import json

class YearRange:    
    def __init__(self, start_year: int, end_year: int):
        self.start_year = start_year
        self.end_year = end_year
    
    @classmethod
    def from_string(cls, range_str: str):
        
        pattern = r'\[(\d{4})-(\d{4})\]'
        match = re.search(pattern, range_str)
        
        if match:
            start_year = int(match.group(1))
            end_year = int(match.group(2))
            return cls(start_year, end_year)
        else:
            return None
    
    def to_dict(self):
        return {
            "startYear": self.start_year,
            "endYear": self.end_year
        }
    
    def to_json(self, indent=2):
        return json.dumps(self.to_dict(), indent=indent)

    def __contains__(self, year):
        return self.start_year <= year <= self.end_year
    
    def __str__(self):
        return f"{self.start_year}-{self.end_year}"