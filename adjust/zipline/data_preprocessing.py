import trading_calendars as tc
from config.settings import ENGINE_PREPROCESSING
import pandas as pd


conn = ENGINE_PREPROCESSING.connect()
sql = """SELECT * FROM tb_adjust_data WHERE ticker= 'AAPL' """
data = pd.read_sql(sql, conn)
print(data)