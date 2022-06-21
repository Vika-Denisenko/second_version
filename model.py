from dataclasses import dataclass
from decimal import Decimal


@dataclass
class ProductInfo:
    name: str
    brand: str = ''
    product_code: str = ''
    price: Decimal = 0
    description: str = ''
    '''Убрать url and qty'''
    url: str = ''
    qty: int = 0