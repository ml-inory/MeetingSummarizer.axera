from fastapi import FastAPI
import uvicorn
import json
import argparse

from asr.factory import ASRFactory

from contextlib import asynccontextmanager
from app.routers.audio import transcriptions


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", type=int, default=8899)
    parser.add_argument("--config", type=str, default="config.json")
    return parser.parse_args()


def load_models(config):
    # ASR
    asr_model = ASRFactory.create(config['transcriptions'].get('model', 'sensevoice'))

    return {
        'transcriptions': asr_model
    }


args = get_args()

with open(args.config, 'r') as f:
    config = json.load(f)

# A simple object to store state
class Model:
    def __init__(self, config):
        self.models = load_models(config)

    def __getitem__(self, model_type):
        return self.models[model_type]
    

state_obj = Model(config)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize the state object at startup
    app.state.ml_model = state_obj
    yield
    # Optional clean up at shutdown
    app.state.ml_model = None

app = FastAPI(lifespan=lifespan)

app.include_router(transcriptions.router)

@app.get("/")
async def root():
    return {"message": "Hello OpenAI server!"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=args.port)