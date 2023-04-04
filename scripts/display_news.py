import logging
import json
from typing import Dict


class Output_data:
    def __init__(self, data: Dict) -> None:
        self.data = data

    def output_info(self) -> None:
        """Displaying information in text format."""
        logging.info('Displaying information in text format')
        for item in self.data:
            print(f"Title:{item['Title']}\nData:{item['Date']}\nLink:{item['Link']}\n")
            print(f"{item['Text']}\n\n")
            print(f"Links:\n[1]:{item['Links']}(link)\n[2]:{item['Image']}(image)\n----\n\n")

    def output_json(self) -> None:
        """Displaying information in json format."""
        logging.info('Displaying information in json format')
        print(json.dumps(self.data, indent=4))
