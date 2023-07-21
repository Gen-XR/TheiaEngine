from typing import List
from io import BytesIO
import requests
import random
import string

from ..utils.response_collections import TheiaResponse


class TheiaPayload:
    def __init__(self):
        self.__questions: List[str] = []
        self.__return_vehicles: bool = False
        self.__return_human_analysis: bool = False
        self.__return_ocr:bool = False
        self.__return_objects:bool = False
        self.__image: BytesIO = None
    
    @property
    def questions(self):
        return self.__questions
    
    @questions.setter
    def questions(self, questions: List[str]):
        self.__questions = questions

    @property
    def return_vehicles(self):
        return self.__return_vehicles
    
    @return_vehicles.setter
    def return_vehicles(self, return_vehicles: bool):
        self.__return_vehicles = return_vehicles
    
    @property
    def return_human_analysis(self):
        return self.__return_human_analysis
    
    @return_human_analysis.setter
    def return_human_analysis(self, return_human_analysis: bool):
        self.__return_human_analysis = return_human_analysis
    
    @property
    def return_ocr(self):
        return self.__return_ocr
    
    @return_ocr.setter
    def return_ocr(self, return_ocr: bool):
        self.__return_ocr = return_ocr
    
    @property
    def return_objects(self):
        return self.__return_objects
    
    @return_objects.setter
    def return_objects(self, return_objects: bool):
        self.__return_objects = return_objects
    
    @property
    def image(self):
        return self.__image
    
    @image.setter
    def image(self, image_input: BytesIO):
        self.__image = image_input


class TheiaClient:
    def __init__(self, api_key: str, theia_url: str) -> None:
        self.__api_key = api_key
        self.__theia_url = theia_url
    
    def inference(self, payload: TheiaPayload) -> TheiaResponse:
        file_name = ''.join(random.choice(string.ascii_letters) for i in range(12))
        files = [
            ("files", (f"{file_name}.jpg", payload.image))
        ]

        r = requests.post(
            self.__theia_url,
            files=files,
            params={
                "questions": ";".join(payload.questions), 
                "api_key": self.__api_key,
                "return_vehicles": payload.return_vehicles,
                "return_human_analysis": payload.return_human_analysis,
                "return_ocr": payload.return_ocr,
                "return_objects": payload.return_objects,
            }, timeout=600
        )

        response_dict = dict(r.json()) if r.status_code in [200, 202, 400, 401, 500] else {"message": "An error occured"}

        return TheiaResponse(
            status_code=r.status_code, response=response_dict
        )