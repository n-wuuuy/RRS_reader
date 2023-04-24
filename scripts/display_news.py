import logging
import json
from typing import Dict
from colorama import Fore
import colorama


class Output_data:
    def __init__(self, data: Dict, colorize: bool = False) -> None:
        self.data = data
        self.colorize = colorize
        colorama.init(autoreset=True)

    def output_info(self) -> None:
        """Displaying information in text format."""
        logging.info('Displaying information in text format')
        for item in self.data:
            print("{3}Title:{4}{0}\n{3}Data:{4}{1}\n{3}Link:{4}{2}\n".format(item['Title'],
                                                                             item['Date'],
                                                                             item['Link'],
                                                                             Fore.RED if self.colorize else Fore.RESET,
                                                                             Fore.RESET))
            print("{0}\n".format(item['Text']))
            print("{2}Links:\n[1]:{0}(link)\n[2]:{1}(image)\n\n\n".format(item['Links'],
                                                                          item['Image'],
                                                                          Fore.CYAN if self.colorize else Fore.RESET))

    def output_json(self) -> None:
        """Displaying information in json format."""
        logging.info('Displaying information in json format')
        print(json.dumps(self.data, indent=4))
