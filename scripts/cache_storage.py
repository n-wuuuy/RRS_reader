import logging
import sqlite3
from datetime import datetime
from operator import itemgetter


class CacheStorage:
    """Cache RSS news."""

    def __init__(self, source: str) -> None:
        """Initialze cache storage."""
        self.source = source

    def init_database(self, path_storage: str) -> None:
        """Initialize database."""
        connection = sqlite3.connect(path_storage)
        curs = connection.cursor()
        curs.execute('''CREATE TABLE IF NOT EXISTS stocks
            (title TEXT, date TEXT, link TEXT, description TEXT, links TEXT, image TEXT )''')
        connection.commit()
        connection.close()
        logging.info('Successful initialze RSS cache database')

    def delete(self, path_storage: str) -> None:
        """Removes data from the database."""
        connection = sqlite3.connect(path_storage)
        connection.execute('DROP TABLE IF EXISTS stocks')
        connection.commit()
        connection.close()


class WriteCache(CacheStorage):
    """Class write cache news."""
    def __init__(self, source: str, new_data: list):
        """Initialze cache writing."""
        super().__init__(source)
        self.news_data = new_data

    def cache_new_list(self, path_storage: str) -> None:
        """Filling the cache in the database."""
        connection = sqlite3.connect(path_storage)
        curs = connection.cursor()
        curs.executemany('INSERT INTO stocks VALUES(?,?,?,?,?,?) ', (self.news_data))
        connection.commit()
        connection.close()


class ReadCache(CacheStorage):
    """Class read cache news."""
    def __init__(self, source: str, date: datetime) -> None:
        """Initialze cache reading."""
        super().__init__(source)
        self.date = date.strftime('%Y%m%d')

    def read_cache(self, path_storage: str):
        """Read Cache from database."""
        connection = sqlite3.connect(path_storage)
        curs = connection.cursor()
        logging.info('Start read')
        news_cache = curs.execute('SELECT * FROM stocks WHERE date >= ?', (self.date, )).fetchall()
        logging.info('Read all from db ')
        connection.close()
        return sorted(news_cache, key=itemgetter(1), reverse=True)