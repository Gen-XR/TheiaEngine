from enum import Enum
from typing import Dict, List, Union, Any


class TheiaResponseStatus(str, Enum):
    SUCCESS = "successful"
    FAILED = "failed"

class TheiaResult:
    def __init__(self, response: Dict[str, Union[str, List[Any], Dict[str, Any]]]):
        self.image_id: str = response["image_id"]
        self.image_name: str = response["image_name"]
        self.description: str = response["description"]
        self.detections: List[Dict[str, Union[str, List[Any], Dict[str, Any]]]] = response["detections"]
        self.ocr: List[Dict[str, Union[str, List[Any], Dict[str, Any]]]] = response["ocr"]
        self.questions: List[Dict[str, str]] = response["questions"]

class TheiaResponse:
    def __init__(self, response: Dict[str, Union[str, List[Any], Dict[str, Any]]], status_code: int):
        self.status: TheiaResponseStatus = TheiaResponseStatus.SUCCESS if status_code in [200, 202] else TheiaResponseStatus.FAILED
        self.result: TheiaResult = None if self.status == TheiaResponseStatus.FAILED else TheiaResult(response["result"])
        self.message: str = response["message"]