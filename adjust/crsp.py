from sqlalchemy import create_engine
import pandas as pd
from config.settings import ENGINE

class CRSP:
    conn = None
    ncusip = None
    data = None

    def __init__(self, ncusip: str):
        self.conn = ENGINE.connect()
        self.ncusip = ncusip
        self.data = self.__get_data()
        self.data['adj_ratio'] = self.__calculate_adjust_ratio()

    def __get_data(self):
        sql = f"""SELECT date,
                   TSYMBOL as ticker,
                   BIDLO   as low,
                   ASKHI   as high,
                   PRC     as close,
                   OPENPRC as open,
                   VOL     as volume,
                   SHROUT  as share,
                   RET     as profit
            FROM tb_daily_stock
            WHERE NCUSIP = '{self.ncusip}' AND DATE > 19950101;
            """
        result = pd.read_sql(sql, self.conn)
        result.dropna(subset=['close', 'profit'], inplace=True)
        result.set_index('date', inplace=True)
        result.index = pd.to_datetime(result.index, format='%Y%m%d')
        return result

    def get(self):
        self.data['adj_close'] = self.data['close'] * self.data['adj_ratio']
        self.data['adj_open'] = self.data['open'] * self.data['adj_ratio']
        self.data['adj_high'] = self.data['high'] * self.data['adj_ratio']
        self.data['adj_low'] = self.data['low'] * self.data['adj_ratio']
        self.data['adj_volume'] = self.data['volume'] / self.data['adj_ratio']
        return self.data.reset_index().set_index(['date', 'ticker'])

    def __calculate_adjust_ratio(self):
        value = self.data['profit'].shift(-1) + 1
        adjust_price = (1 / value).iloc[::-1].cumprod().iloc[::-1] * abs(self.data['close'].iloc[-1])
        adjust_price.iloc[-1] = self.data['close'].iloc[-1]
        adjust_ratio = adjust_price / self.data['close']
        return adjust_ratio

