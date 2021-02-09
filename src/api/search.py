from pydantic import BaseModel

from wrappers import cobs


class Body(BaseModel):
    query: str


class OccurrenceResponse(BaseModel):
    number_of_occurrences: int
    document_name: str


async def request(body: Body):
    r = cobs.search(body.query)
    return [OccurrenceResponse(
        number_of_occurrences=o, document_name=d
    ) for o, d in r]
