from pydantic import BaseModel


class SearchRequest(BaseModel):
    document: str


class SearchResponse(BaseModel):
    msg: str


class ExtractedResponse(BaseModel):
    id: str
    documento: str
    fecha_creacion: str
    procesos: list


class ExtractedResumeResponse(BaseModel):
    id: str
    documento: str
    fecha_creacion: str
    cantidad_procesos: list
