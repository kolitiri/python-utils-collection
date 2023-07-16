import functools
import json
from typing import Any, Dict, Optional
import unittest

from exceptions import InvalidJsonTypeError, MissingTransformersError
from transformer import MsgTransformer, requiredtransformer


class HSBCTransformer(MsgTransformer):
    """ Transformer class for 'HSBC' messages """
    json_type: str = 'HSBC'

    def _validate_json_type(self, message: Dict[str, Any]):
        if message.get('correspondence') != 'HSBC Bank USA':
            raise InvalidJsonTypeError(self.json_type)

    @requiredtransformer
    def replace_account_number(
        self, message: Dict[str, Any], account_number: Optional[str] = None
    ) -> Dict[str, Any]:
        message['accountNumber'] = account_number
        return message

    def replace_account_name(
        self, message: Dict[str, Any], account_name: Optional[str] = None
    ) -> Dict[str, Any]:
        message['accountName'] = account_name
        return message


class TestTransformer(unittest.TestCase):
    def setUp(self):
        with open('example_json/hsbc_statement.json', 'r') as json_file:
            self.hsbc_json = json.loads(json_file.read())

    def test_transformation_success(self):
        expected_transformed_json = {
            'correspondence': 'HSBC Bank USA',
            'accountName': 'Jane Doe',
            'accountNumber': 'ABC123',
            'openingBalance': 3000,
            'transactions': [
                {
                    'description': 'Transfer from sort code 20-10-33',
                    'datetime': '2023-01-01: 14:06:00',
                    'details': 'Credit',
                    'amount': 120
                },
                {
                    'description': 'Payment to XYZ',
                    'datetime': '2023-01-02: 10:05:10',
                    'details': 'Debit',
                    'amount': 15
                }
            ]
        }

        hsbc_transformer = HSBCTransformer()
        transformed_json = hsbc_transformer.transform(
            self.hsbc_json,
            transformers=[
                functools.partial(hsbc_transformer.replace_account_number, account_number="ABC123"),
                functools.partial(hsbc_transformer.replace_account_name, account_name="Jane Doe")
            ]
        )

        self.assertEqual(transformed_json, expected_transformed_json)

    def test_transformation_failure_missing_transformer(self):
        with self.assertRaises(MissingTransformersError):
            hsbc_transformer = HSBCTransformer()
            hsbc_transformer.transform(
                self.hsbc_json,
                transformers=[
                    functools.partial(hsbc_transformer.replace_account_name, account_name="Jane Doe")
                ]
            )


if __name__ == '__main__':
    unittest.main()
