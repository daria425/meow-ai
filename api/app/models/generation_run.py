from pydantic import BaseModel
from typing import List
class EvaluationDict(BaseModel):
    similarity_to_original: str
    cuteness_factor: str
    artistic_style: str
    overall_impression: str

class EvaluationData(BaseModel):
    evaluation:EvaluationDict
    critique: str

class RunData(BaseModel):
    iteration_num: int
    prompt: str
    cartoonized_image: str
    evaluation: EvaluationData



class GenerationRun(BaseModel):
    original_image_url: str
    runs: List[RunData] = []
