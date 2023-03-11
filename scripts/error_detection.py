import logging

class MyCustomError(Exception):
    def __init__(self, message:str) -> None:
        self.message=message
        logging.exception('{}. RSS reader error'.format(message))

class MyCustomCriticalError(Exception):
    def __init__(self, message:str) -> None:
        self.message=message
        logging.critical('{}. RSS reader error'.format(message))