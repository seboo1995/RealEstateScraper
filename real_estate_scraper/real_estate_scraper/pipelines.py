from scrapy import signals
from pydispatch import dispatcher
import psycopg2
from dotenv import dotenv_values
from itemadapter import ItemAdapter
from pymongo import MongoClient


config = dotenv_values("../../.env")
host = config.get('host')
user = config.get('user')
database = config.get('database')
password = config.get('password')
mongo_conn_string = config.get('mongo_conn_string')
print(mongo_conn_string)


class Reklama5Pipeline:
    def __init__(self):
        self.create_connection()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def create_connection(self):
        self.client = MongoClient(mongo_conn_string)
        database = self.client['reklama5data']
        self.collection = database['apartments']

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.collection.insert_one(dict(item))

    def spider_closed(self, spider, reason):
        print('CONN IS CLOSEDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
        self.client.close()


class Pazar3Pipeline:
    def __init__(self):
        self.create_connection()
        dispatcher.connect(self.spider_closed, signals.spider_closed)

    def create_connection(self):
        self.conn = psycopg2.connect(
            database=database,
            user=user,
            password=password,
            host=host
        )
        self.curr = self.conn.cursor()

    def spider_closed(self, spider, reason):
        self.conn.close()

    def process_item(self, item, spider):
        self.store_db(item)
        return item

    def store_db(self, item):
        self.curr.execute('''
            INSERT INTO pazar3data VALUES(%s,%s,%s,%s,%s,%s)''', (
            item['title'],
            item['price'],
            item['num_of_rooms'],
            item['area'],
            item['location'],
            item['link']
        ))
        self.conn.commit()
