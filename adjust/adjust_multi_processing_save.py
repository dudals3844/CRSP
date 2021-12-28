from multiprocessing import Pool

import numpy as np
from sqlalchemy import Table
from adjust.crsp import CRSP
from adjust.models import AdjustDataModel
from config.settings import ENGINE, ENGINE_PREPROCESSING, META
import pandas as pd

def start(ncusip: str):
    try:
        conn = ENGINE_PREPROCESSING.connect()
        table = Table(AdjustDataModel.__tablename__, META, autoload_with=ENGINE_PREPROCESSING)
        crsp = CRSP(ncusip)
        data = crsp.get()
        data = data.replace({np.nan: None})
        data = data.reset_index()
        data['ticker'] = data['ticker'].fillna(method='bfill')
        dict_data = data.to_dict('records')
        conn.execute(table.insert().prefix_with('IGNORE'), dict_data)
        del conn
    except Exception as e:
        print(e)



if __name__ == "__main__":
    sql = """SELECT DISTINCT (NCUSIP) FROM tb_names WHERE EXCHCD IN (1,2,3,4);"""
    ncusips = pd.read_sql(sql, ENGINE.connect())['NCUSIP']
    pool = Pool(processes=1)
    pool.map(start, ncusips)
    pool.close()
    pool.join()
