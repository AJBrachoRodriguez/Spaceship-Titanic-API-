from pydantic import BaseModel
import numpy as np

class Prediction_Input(BaseModel):
    flag : str
    id : int
    input_parameter : str


class Prediction_Output(BaseModel):
    flag : str
    id : int
    input_parameter_used : str    #Prediction_Input.input_parameter
    prediction : list


## this is donesaksaksnaksa 