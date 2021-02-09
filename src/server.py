from typing import List

from fastapi import FastAPI

from api import search, build

app = FastAPI()

app.post(
    '/search',
    response_model=List[search.OccurrenceResponse]
)(search.request)

app.post(
    '/build'
)(build.request)
