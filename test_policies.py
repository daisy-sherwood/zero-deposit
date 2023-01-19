from datetime import date
from unittest import TestCase, main
from unittest.mock import patch

import policies


class TestGuarantee(TestCase):

    def test_future_date(self):
        json_object = {'address': '83609 Nicholas Freeway Suite 376', 'end_date': '2026-05-28'}
        days_left = policies.return_guarantee(json_object, False)
        self.assertGreater(days_left, 0)

    def test_past_date(self):
        json_object = {'address': '83609 Nicholas Freeway Suite 376', 'end_date': '2021-05-28'}
        days_left = policies.return_guarantee(json_object, False)
        self.assertLess(days_left, 0)

    def test_today_date(self):
        today_date = date.today().isoformat()
        json_object = {'address': '83609 Nicholas Freeway Suite 376', 'end_date': today_date}
        days_left = policies.return_guarantee(json_object, False)
        self.assertEqual(days_left, 0)

    def test_incorrect_date(self):
        json_object = {'address': '83609 Nicholas Freeway Suite 376', 'end_date': '2023-04-31'}
        days_left = policies.return_guarantee(json_object, False)
        self.assertEqual(days_left, None)

    def test_empty_date(self):
        json_object = {'address': '83609 Nicholas Freeway Suite 376', 'end_date': ''}
        days_left = policies.return_guarantee(json_object, False)
        self.assertEqual(days_left, None)

    def test_empty_address(self):
        json_object = {'address': '', 'end_date': '2023-01-18'}
        days_left = policies.return_guarantee(json_object, False)
        self.assertEqual(days_left, None)

    def test_missing_date_field(self):
        json_object = {'address': '83609 Nicholas Freeway Suite 376'}
        days_left = policies.return_guarantee(json_object, False)
        self.assertEqual(days_left, None)

    def test_missing_address_field(self):
        json_object = {'end_date': '2023-01-18'}
        days_left = policies.return_guarantee(json_object, False)
        self.assertEqual(days_left, None)

    def test_extended_true(self):
        json_object = {'address': '83609 Nicholas Freeway Suite 376', 'end_date': '2026-05-28'}
        days_left = policies.return_guarantee(json_object, True)
        self.assertGreater(days_left, 0)


class TestGetData(TestCase):

    def test_response_type(self):
        response = policies.get_data()
        self.assertIsInstance(response, list)

    def test_response_not_empty(self):
        response = policies.get_data()
        self.assertGreater(len(response), 0)


class TestExtended(TestCase):

    @patch('sys.argv', ['policies.py'])
    def test_no_arguments(self):
        self.assertFalse(policies.check_if_extended())

    @patch('sys.argv', ['policies.py', 'incorrect'])
    def test_incorrect_argument(self):
        self.assertFalse(policies.check_if_extended())

    @patch('sys.argv', ['policies.py', 'extend'])
    def test_correct_argument(self):
        self.assertTrue(policies.check_if_extended())


if __name__ == '__main__':
    main()
