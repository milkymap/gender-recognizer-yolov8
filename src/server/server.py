import cv2 
import numpy as np 

import asyncio
import uvicorn

from ultralytics import YOLO

from fastapi import FastAPI
from fastapi import HTTPException, UploadFile, File 
from fastapi.responses import JSONResponse

class APIServer:
    def __init__(self, host:str, port:int, model_name:str, mounting_path:str):
        self.host = host 
        self.port = port 
        self.model_name = model_name
        self.mounting_path = mounting_path
        self.app = FastAPI(
            docs_url='/',
            title='gender-recognition',
            version='0.0.1',
            description='gender recognition api based on yolov8'
        ) 

        self.model = YOLO(model=model_name)

    def define_routes(self):
        self.app.add_api_route('/heartbit', self.heartbit)
        self.app.add_api_route('/predict_gender', self.predict, methods=['POST'])

    async def heartbit(self): 
        return JSONResponse(
            status_code=200,
            content={
                'contents': f'server is running at port {self.model_name}'
            }
        )

    async def predict(self, threshold:float=0.1, image:UploadFile=File()):
        binarystream = await image.read()
        bgr_image = cv2.imdecode(np.frombuffer(binarystream, np.uint8), cv2.IMREAD_COLOR)
        outputs = self.model(bgr_image, classes=[0, 1], conf=threshold)
        data = outputs[0].boxes.cpu().numpy().data
    
        boxes = data[:, :4].astype('int32').tolist()
        score = data[:, 4].tolist()
        index = data[:, 5].tolist()
        return JSONResponse(
            status_code=200,
            content={
                'boxes': boxes, 
                'score': score,
                'index': index
            }
        )

    async def listen(self):
        self.config = uvicorn.Config(app=self.app, host=self.host, port=self.port, root_path=self.mounting_path)
        self.server = uvicorn.Server(self.config)
        await self.server.serve()


def launch_server(host:str, port:int, model_name:str, mounting_path:str):
    async def _main():
        server = APIServer(host=host, port=port, model_name=model_name, mounting_path=mounting_path)
        server.define_routes()
        await server.listen()
    
    asyncio.run(main=_main())