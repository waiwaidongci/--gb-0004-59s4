from datetime import date
from pydantic import BaseModel,Field
class ObservationInput(BaseModel):
    day:date
    value:float=Field(ge=0,le=10000000,allow_inf_nan=False)
