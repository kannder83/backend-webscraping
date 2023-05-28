import asyncio
import logging
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from pydantic import BaseModel

from app.pages_scraping.judicatura import Judicatura

router = APIRouter()


class SearchRequest(BaseModel):
    document: str


async def perform_search(document):
    judicatura = Judicatura(values=document)
    judicatura.search()
    # Puedes realizar cualquier tarea adicional aquí mientras esperas que se complete judicatura.search()


@router.post(
    "/search",
    response_model=dict,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Realizar consulta por documento."
)
async def search(document: str, background_tasks: BackgroundTasks):
    try:

        response_message = {"process": f"Se encola el documento: {document}"}
        logging.info(f"Response: {response_message}")
        background_tasks.add_task(perform_search, document)

        return response_message
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"error": str(error)}
        )
