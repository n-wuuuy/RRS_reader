import argparse
import data_parser
import logging


class RSSReader:
    '''Program executing class.'''
    def __init__(self) -> None:
        '''Initialze RSSReader class.'''
        self.argument = self.parse_argument()
        if self.argument.verbose:
            self.turn_on_verbose()

    def parse_argument(self) -> None:
        '''Parse application arguments.'''
        argument_parser = argparse.ArgumentParser(description='Pure Python command-line RSS reader.')
        argument_parser.add_argument('source',
                                     help='RSS URL',
                                     type=str)
        argument_parser.add_argument('--version',
                                     help='Print version info',
                                     action='version',
                                     version='%(prog)s v1.0')
        argument_parser.add_argument('--json',
                                     help='Print result as JSON in stdout',
                                     action='store_true')
        argument_parser.add_argument('--verbose',
                                     help='Outputs verbose status messages',
                                     action='store_true')
        argument_parser.add_argument('--limit',
                                     help='Limit news topics if this parameter provided',
                                     type=int)
        return argument_parser.parse_args()

    def turn_on_verbose(self) -> None:
        '''Enable verbose mode.'''
        logging.basicConfig(level=logging.INFO)

    def executable_rrs_reader(self) -> None:
        '''Execute RSS reader application.'''
        def information_display() -> None:
            '''Displays information on the screen.'''
            rss_reader = data_parser.DataParser(self.argument.source)
            rss_reader.fill_information()
            rss_reader.data = rss_reader.data[:self.argument.limit]
            if self.argument.json:
                rss_reader.output_json()
            else:
                rss_reader.output_info()
        information_display()

    def run_rss_reader(self) -> None:
        '''Launches the application.'''
        self.executable_rrs_reader()


if __name__ == '__main__':
    rss_reader = RSSReader()
    rss_reader.run_rss_reader()