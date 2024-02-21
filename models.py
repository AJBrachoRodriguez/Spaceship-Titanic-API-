from pydantic import BaseModel
import numpy as np

class Prediction_Input(BaseModel):
    db_id : int
    additional_comment : str

class Prediction_Output(BaseModel):
    db_id : int
    additional_comment : str    #Prediction_Input.input_parameter
