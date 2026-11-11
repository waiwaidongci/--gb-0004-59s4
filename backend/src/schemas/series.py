from pydantic import BaseModel,Field
class SeriesInput(BaseModel):
    code:str=Field(min_length=2,max_length=60,pattern=r'^[a-z0-9-]+$')
    name:str=Field(min_length=2,max_length=100)
    city:str=Field(min_length=1,max_length=40)
    product:str=Field(min_length=1,max_length=60)
