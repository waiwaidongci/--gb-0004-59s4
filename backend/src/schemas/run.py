from pydantic import BaseModel,Field
class RunInput(BaseModel):
    name:str=Field(min_length=2,max_length=100)
    series_id:int=Field(gt=0)
    horizon:int=Field(default=14,ge=1,le=30)
    season:int=Field(default=7,ge=2,le=30)
