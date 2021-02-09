from pydantic.main import BaseModel

from wrappers import cobs


class Body(BaseModel):
    cobs_document_dir_path: str
    cobs_output_path: str
    cobs_term_size: int
    cobs_clobber: bool
    cobs_false_positive_rate: float


async def request(body: Body):
    cobs.build(body.cobs_document_dir_path, body.cobs_output_path, body.cobs_term_size, body.cobs_clobber,
               body.cobs_false_positive_rate)
    return body
