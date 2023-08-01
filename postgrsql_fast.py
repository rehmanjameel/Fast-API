from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from typing import List, Annotated


app = FastAPI()


# questions choice model class
class ChoiceBase(BaseModel):
    choice_text: str
    is_correct: bool


# questions model class
class QuestionBase(BaseModel):
    question_text: str
    choices: List[ChoiceBase]



