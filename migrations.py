from config.settings import ENGINE_PREPROCESSING
from adjust.models import AdjustDataModel

AdjustDataModel.__table__.create(bind=ENGINE_PREPROCESSING, checkfirst=True)

