import decimal

from .constants import CODE_TYPE_CHOICES
from .models import Code


class GetDiscountPrice:
    def __init__(self, price: decimal.Decimal, code: str):
        self._price = price
        self._code = code
        self._reduction_amount = 0

    def execute(self) -> decimal.Decimal:
        code = Code.objects.get(code=self._code)
        amount_to_be_deducted = self._get_amount_to_be_deducted(code=code)
        deducted_amount = self._price - amount_to_be_deducted

        if deducted_amount < 0:
            return decimal.Decimal("0")
        else:
            return deducted_amount

    def _get_amount_to_be_deducted(self, code: Code) -> decimal.Decimal:
        if code.type == CODE_TYPE_CHOICES["flat"]:
            return code.amount
        else:
            return code.amount * self._price / 100
