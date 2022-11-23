from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.exception import SensorException
import os,sys
import shutil
from sensor.logger import logging
from sensor.pipeline import training_pipeline
from sensor.pipeline.training_pipeline import TrainPipeline
from sensor.utils.main_utils import read_yaml_file
from sensor.constant.training_pipeline import SAVED_MODEL_DIR
from fastapi import FastAPI,UploadFile,File
from sensor.constant.application import APP_HOST,APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from fastapi.responses import Response
from sensor.ml.model.estimator import ModelResolver,TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        training_pipeline = TrainPipeline()
        if training_pipeline.is_pipeline_running:
            return Response("Training pipeline is already running.")
        training_pipeline.run_pipeline()
        return Response("Training successfull..!!!")
    except Exception as e:
        return Response(f"Error Occured! {e}")

        
@app.post("/upload")
def upload(file: UploadFile = File(...)):
    try:
        with open(file.filename, 'wb') as f:
            shutil.copyfileobj(file.file, f)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()
        
    return {"message": f"Successfully uploaded {file.filename}"}

@app.get("/predict")
async def predict_route(file):
    try:
        
        df = file
        model_resolver = ModelResolver(model_dir = SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
            return Response("Model is not available")

        best_model_path = model_resolver.get_best_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df['predicted_column'] = y_pred
        df['predicted_column'].replace(TargetValueMapping().reverse_mapping(),inplace=True)
               

    except Exception as e:
        raise Response(f"Error Occured! {e}")

def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)

if __name__=="__main__":
    app_run(app, host=APP_HOST, port=APP_PORT)