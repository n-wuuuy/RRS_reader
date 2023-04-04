import argparse
from data_parser import DataParser
import logging
from datetime import datetime
from typing import List, Dict
from cache_storage import ReadCache, WriteCache
from display_news import Output_data


class RSSReader:
    """Program executing class."""
    def __init__(self) -> None:
        """Initialze RSSReader class."""
        self.argument = self.parse_argument()
        if self.argument.verbose:
            self.turn_on_verbose()

    def parse_argument(self) -> None:
        """Parse application arguments."""
        def validate_date(cache_date: str) -> datetime:
            """Validate cache date for '--date' argument."""
            try:
                return datetime.strptime(cache_date, '%Y%m%d')
            except ValueError:
                raise argparse.ArgumentTypeError(f'Incorrect cache date: {cache_date}')

        argument_parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
        argument_parser.add_argument('source',
                                     help='RSS URL',
                                     type=str)
        argument_parser.add_argument('--version',
                                     help='Print version info',
                                     action='version',
                                     version='%(prog)s v3.0')
        argument_parser.add_argument('--json',
                                     help='Print result as JSON in stdout',
                                     action='store_true')
        argument_parser.add_argument('--verbose',
                                     help='Outputs verbose status messages',
                                     action='store_true')
        argument_parser.add_argument('--limit',
                                     help='Limit news topics if this parameter provided',
                                     type=int)
        argument_parser.add_argument('--date',
                                     help=r'Display cached news for the specified date (date format - \'YYYYmmDD\')',
                                     type=validate_date)
        return argument_parser.parse_args()

    def turn_on_verbose(self) -> None:
        """Enable verbose mode."""
        logging.basicConfig(level=logging.INFO)

    def executable_rrs_reader(self) -> None:
        """Execute RSS reader application."""
        def information_display(data_output: Dict) -> None:
            """Displays information on the screen."""
            output_info = Output_data(data_output)
            if self.argument.json:
                output_info.output_json()
            else:
                output_info.output_info()

        def get_news_data() -> List:
            """Get news data from database"""
            if self.argument.date:
                get_data = ReadCache(self.argument.source, self.argument.date)
                untransformed_cache_data = get_data.read_cache('RSSDB.db')
                cache_data = conver_data_output(untransformed_cache_data)
                get_data.delete('RSSDB.db')
            else:
                rss_reader = DataParser(self.argument.source)
                rss_reader.fill_information()
                cache_data = rss_reader.data
            return cache_data

        def cache_news_data() -> None:
            """Cache news data to database."""
            rss_reader = DataParser(self.argument.source)
            rss_reader.fill_information()
            transformed_data = [[data.get('Title'),
                                 date_conversion(data.get('Date')),
                                 data.get('Link'),
                                 data.get('Text'),
                                 (data.get('Links')),
                                 (data.get('Image'))]for data in rss_reader.data]
            write_cache = WriteCache(self.argument.source,  transformed_data)
            write_cache.init_database('RSSDB.db')
            write_cache.cache_new_list('RSSDB.db')

        def date_conversion(data: str) -> str:
            """Convert date to '--date' format."""
            datetime_object = datetime.strptime(data, '%a, %d %b %Y %X %z')
            return datetime_object.strftime("%Y%m%d")

        def conver_data_output(data_list: List) -> Dict:
            """Converts data from a database into a usable format"""
            correct_data = []
            for data in data_list:
                correct_data.append({'Title': data[0],
                                     'Date': data[1],
                                     'Link': data[2],
                                     'Text': data[3],
                                     'Links': data[4],
                                     'Image': data[5]})
            return correct_data

        cache_news_data()
        cache_data = get_news_data()
        if not cache_data:
            print('No news in the selected source with specified application parameters')
            return
        news_data = cache_data[:self.argument.limit]
        information_display(news_data)

    def run_rss_reader(self) -> None:
        """Launches the application."""
        self.executable_rrs_reader()


def run() -> None:
    """Allow to run CLI apllication 'RSS reader' as 'rss-reader' in console. Uses in 'setup.py'."""
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()


if __name__ == '__main__':
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()