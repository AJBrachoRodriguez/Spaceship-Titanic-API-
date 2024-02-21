import pandas as pd
import numpy as np
import pickle
from fastapi import APIRouter
from models import Prediction_Input
from models import Prediction_Output


MODEL_PATH = "model.pkl"
SCALER_PATH = "scaler.pkl"
DATASET_PATH = "test.csv"


# 1. Load the 'test' dataset to predict
dataset_filename = DATASET_PATH
set = pd.read_csv(dataset_filename)
df_set = pd.DataFrame(set)
X = df_set['CryoSleep']

# 1.1 Preprocessing the data
X = X.dropna(axis=0,how='any')
X = X.replace({False:0,True:1})
X = np.array(X).reshape(-1,1)
print(type(X), X.shape, X.ndim)


# 2. Load the model
with open('model.pkl','rb') as f:
    model = pickle.load(f)

# 3. Load the scaler
scaler_filename = SCALER_PATH
with open(scaler_filename,"rb") as f:
    scaler = pickle.load(f)

router = APIRouter()

database = []


#### GET ####
@router.get('/ml')
def get_prediction():
    return database


#### POST ####
@router.post('/ml', status_code=201)
def make_prediction(pred_input:Prediction_Input):
    X_test = scaler.transform(X)
    y_pred = model.predict(X_test)
    predictions = y_pred.tolist()
    new_prediction = { 
           'flag':f"prediction done with id {pred_input.db_id}",
           'id':pred_input.db_id,
           'additional_comment': pred_input.additional_comment,
           'predictions': predictions
    }
    database.append(new_prediction)
    return new_prediction


#### PUT ####
@router.put('/ml/{db_id}')
def update_db_id(put :Prediction_Output):    
    for element_db_index,element_db_value in enumerate(database):
        if element_db_value["id"] == put.db_id:
            del element_db_value["predictions"]
            X_test = scaler.transform(X)
            y_pred = model.predict(X_test)
            predictions = y_pred.tolist()
            element_db_value["flag"]= f"updated prediction on id {put.db_id}"
            element_db_value["id"]=put.db_id
            element_db_value['additional_comment']= put.additional_comment
            element_db_value["predictions"]= predictions
            return 'The update has been done!'
    else:
        return "db_id not found!"


#### DELETE ####
@router.delete('/ml/{db_id}')
def delete_past_predictions(db_id:int):
    for element_db_index,element_db_value in enumerate(database):
        if element_db_value["id"] == db_id:
            database.remove(database[element_db_index])
            return f"The prediction with id {db_id} has been deleted!"
    else:
        return "db_id not found!"
