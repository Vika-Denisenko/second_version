from decimal import Decimal


def extract_decimal_price(text: str) -> Decimal:
    """Функция, которая извлекает из строки цену"""

    # text == "$110.00 $122.00\nEx Tax: $90.00"
    split_by_lines: List[str] = text.split("\n")
    # split_by_lines == ["$110.00 $122.00", "Ex Tax: $90.00"]

    first_price_lines = split_by_lines[0].split(' ')
    # first_price == ["$110.00", "$122.00"]

    # Удаляем первый символ (доллар)
    first_price = first_price_lines[0][1:]
    # В случае 1,202.00 нужно убрать запятую.
    first_price_without_punctuation = first_price.replace(",", "")

    return Decimal(first_price_without_punctuation)