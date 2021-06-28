import uuid
from unittest import TestCase

from payments.stk import initiate_stk


class STKTestCase(TestCase):
    def setUp(self) -> None:
        self.phone_number = '254797792447'
        self.redirect_url = 'https://test.edonation/'
        self.amount = 10

    def test_initiate_payments(self):
        response = initiate_stk(
            phone_number=self.phone_number,
            amount=self.amount,
            callback_url=self.redirect_url,
            transaction_id=uuid.uuid4().hex
        )
        print(response.json())
