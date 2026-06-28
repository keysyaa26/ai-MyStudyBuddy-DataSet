from fastapi import FastAPI
from pydantic import BaseModel

<<<<<<< HEAD
<<<<<<< HEAD
from app.inference import summarize
=======
from inference import summarize

>>>>>>> 31bcc8a8376f91270cefcd29697bded76bbf5973
=======
from inference import summarize

>>>>>>> 31bcc8a8376f91270cefcd29697bded76bbf5973
app = FastAPI()

class SummaryRequest(BaseModel):
    text: str

@app.post("/summarize")
def summarize_endpoint(req: SummaryRequest):

    result = summarize(req.text)

    return {
        "summary": result
    }