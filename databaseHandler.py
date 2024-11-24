import os
import traceback
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import sqlitecloud

sAPIKey = os.environ['SQLiteAPIKey']


import re


def df_to_sql_bulk_insert(df: pd.DataFrame, table: str, **kwargs) -> str:
    df = df.copy().assign(**kwargs)
    columns = ", ".join(df.columns)
    tuples = map(str, df.itertuples(index=False, name=None))
    values = re.sub(r"(?<=\W)(nan|None)(?=\W)", "NULL", (",\n" + " " * 7).join(tuples))
    return f"INSERT INTO {table} ({columns})\nVALUES {values};"

class DBHandler():
    def __init__(self):
        self.conn = sqlitecloud.connect(sAPIKey)
        self.conn.execute('USE DATABASE ScrapingRawData')

    def vAddRowsPazar3(self,dfRawData:pd.DataFrame):
        try:
           # dfRawData.to_sql('Pazar3RawData',conn,if_exists='append',index=False)
            sSQL = df_to_sql_bulk_insert(dfRawData,'Pazar3RawData')
            self.conn.execute(sSQL)
            return
        except Exception as e:
            print('Could not add data to Pazar3RawData')
            print(traceback.format_exc())
            return
    def __del__(self):
        self.conn.close()