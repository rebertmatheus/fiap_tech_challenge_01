from dataclasses import dataclass, field
from typing import List, Optional
import json
import re

@dataclass
class Product:
    name: str
    quantity: float
    unit: str
    amount: Optional[float] = 0
    group: Optional[str] = None
    sub_products: List['Product'] = field(default_factory=list)
    
    def is_category(self) -> bool:
        return not self.group
    
    def add_sub_product(self, product: 'Product') -> None:
        self.sub_products.append(product)

    def to_dict(self) -> dict:
        return {
            "name": self.name,
            "quantity": self.quantity,
            "unit": self.unit,
            "amount": self.amount,
            "group": self.group if self.group else "",
            "sub_products": [p.to_dict() for p in self.sub_products]
        }
    
    def to_json(self, indent=2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)
    
    def __str__(self) -> str:
        result = f"{self.name}: {self.quantity} {self.unit} {self.amount}"
        if self.is_category() and self.sub_products:
            result += f" ({len(self.sub_products)} subitens)"
        return result
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Product':
        first_key = list(data.keys())[0]
        name = data.get(first_key, '')

        quantity_key = next((key for key in data.keys() if 'Quantidade' in key), 'Quantidade')
        unit_match = re.search(r'\(([^)]+)\)', quantity_key)
        unit = unit_match.group(1) if unit_match else ""
        
        amount_key = next((key for key in data.keys() if 'Valor' in key), 'Valor')
        
        quantity_str = data.get(quantity_key, '0')
        amount_str = data.get(amount_key, '0')
        
        qty_clean = quantity_str.replace('.', '')
        amount_clean = amount_str.replace('.','')
        try:
            quantity = float(qty_clean)
            amount = float(amount_clean)
        except ValueError:
            quantity = 0.0
            amount = 0.0
        
        group = data.get('Grupo', '')
        
        return cls(
            name=name,
            quantity=quantity,
            unit=unit,
            amount=amount,
            group=group
        )

    @classmethod
    def products_to_json(cls, products: List['Product'], indent=2) -> str:
        categories = {}
        other_products = []
        
        for product in products:
            if product.is_category():
                categories[product.name] = product.to_dict()
            else:
                other_products.append(product)
        
        for product in other_products:
            if not product.group or product.group not in categories:
                continue
            
            for category_name, category_dict in categories.items():
                if product.group == category_name:
                    category_dict["sub_products"].append(product.to_dict())
                    break
        
        result = list(categories.values())
        
        return json.dumps(result, indent=indent, ensure_ascii=False)