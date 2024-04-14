from typing import Dict

from model_utils import Choices

LATEST_ITEMS: int = 4

CATEGORY_MESSAGE = {
    "create_success": "Category create success",
    "create_fail": "Category create fail",
}

ITEM_MESSAGE = {
    "create_success": "Item create success",
    "create_fail": "Item create fail",
}

MANAGER_ERROR_MESSAGES: Dict = {
    "DONE": "done",
    "NOT_ACTIVE": "not active",
    "NO_IMAGES": "no images",
    "NO_ACTIVE_IMAGES": "no active images",
    "NO_SALE_PRICE": "no sale price",
    "NO_ACTIVE_SALE_PRICE": "no active sale price",
}

ABOUT_MESSAGE = """
Hi! We are Kipa Prints. We have awesome collection of t-shirts and phone cases
that we sincerely hope that you would enjoy. We are dedicated to provide the 
best in design and quality.
"""

CUSTOMER_ORDER_CHOICES = Choices(
    ("started", "Order Started"),
    ("dispatched", "Order Dispatched"),
    ("delivered", "Order Delivered"),
    ("cancelled", "Order Cancelled"),
    ("returned_started", "Order Returned Started"),
    ("returned_completed", "Order Returned"),
    ("unknown", "Order Unknown"),
    ("lost", "Order Lost"),
)

ITEM_LOG_TYPE = Choices(
    ("pu", "Purchases"),
    ("sl", "Sales"),
    ("pr", "Purchase Return"),
    ("sr", "Sales Return"),
    ("di", "Item Disposed"),
    ("dr", "Item Disposed Reversed"),
)

RETURN_TYPE = Choices(
    ("full", "Full"),
    ("partial", "Partial"),
)


CODE_TYPE_CHOICES = Choices(
    ("flat", "FLAT"),
    ("percent", "PERCENT"),
)
