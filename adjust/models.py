from config.settings import BASE
from sqlalchemy import Column, DATETIME, FLOAT, INT, VARCHAR, PrimaryKeyConstraint


class AdjustDataModel(BASE):
    __tablename__ = 'tb_adjust_data'
    date = Column(DATETIME, nullable=False)
    ticker = Column(VARCHAR(15), nullable=False)
    low = Column(FLOAT)
    high = Column(FLOAT)
    close = Column(FLOAT)
    open = Column(FLOAT)
    volume = Column(INT)
    share = Column(INT)
    profit = Column(FLOAT)
    adj_ratio = Column(FLOAT)
    adj_low = Column(FLOAT)
    adj_high = Column(FLOAT)
    adj_close = Column(FLOAT)
    adj_open = Column(FLOAT)
    adj_volume = Column(FLOAT)

    __table_args__ = (
        PrimaryKeyConstraint(date, ticker),
        {},
    )

