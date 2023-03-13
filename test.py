import unittest
from unittest import TestCase, mock
from scripts.data_parser import  DataParser


class TestDataParser(TestCase):
    def setUp(self):
        self.source = 'scripts/RSS_checking_lenta'
        self.parser = DataParser(self.source)

    @mock.patch('feedparser.parse')
    def test_check_link(self, mocked_parse):
        mocked_source_data = mock.Mock()
        mocked_source_data.feed = {'Title': 'Test RSS'}
        mocked_source_data.bozo = 0
        mocked_parse.return_value = mocked_source_data
        source_data = self.parser.check_link()
        self.assertEqual(source_data.feed, mocked_source_data.feed, f'Should be \'{mocked_source_data.feed}\'')


if __name__ == '__main__':
    unittest.main()