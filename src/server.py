from typing import List

from fastapi import FastAPI

from api import search


app = FastAPI()

app.post(
    '/search',
    response_model=List[search.OccurrenceResponse]
)(search.request)
