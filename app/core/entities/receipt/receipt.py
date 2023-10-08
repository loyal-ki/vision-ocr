from dataclasses import dataclass, field


@dataclass
class Address:
    house_number: str = ""
    po_box: str = ""
    road: str = ""
    city: str = ""
    state: str = ""
    postal_code: str = ""
    country_region: str = ""
    street_address: str = ""
    unit: str = ""
    city_district: str = ""
    state_district: str = ""
    suburb: str = ""
    house: str = ""
    level: str = ""


@dataclass
class ReceiptItem:
    description: str = ""
    quantity: str = ""
    price: str = ""
    total_price: str = ""


@dataclass
class Receipt:
    merchant_name: str = ""
    transaction_date: str = ""
    transaction_time: str = ""
    address: Address = field(default_factory=Address)
    phone_number: str = ""
    subtotal: str = ""
    tax: str = ""
    tip: str = ""
    total: str = ""
    receipt_items: list[ReceiptItem] = field(default_factory=list)

    def add_receipt_item(self, item):
        self.receipt_items.append(item)
