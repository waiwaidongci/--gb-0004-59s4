from pydantic import BaseModel,Field
class ReleaseInput(BaseModel):
    run_id:int=Field(gt=0)
    note:str=Field(min_length=3,max_length=500)
