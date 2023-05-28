import logging
from pydantic import BaseModel
from bson import ObjectId
from app.web_scraping.models import SearchRequest, SearchResponse, ExtractedResponse, ExtractedResumeResponse
from fastapi import APIRouter, BackgroundTasks, HTTPException, status
from app.web_scraping.controller import db_judicatura


from app.pages_scraping.judicatura import Judicatura

router = APIRouter()


def write_notification(value: str):
    judicatura = Judicatura(values=value)
    judicatura.search()


@router.get(
    path="/store-information/",
    status_code=status.HTTP_200_OK,
    summary="Show all id's of extracted information"
)
async def get_extracted_information(

):
    """
    """
    try:
        get_ids = db_judicatura.get_store_ids()

        return get_ids
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)


@router.get(
    path="/extracted-information/{document_id}",
    response_model=ExtractedResponse,
    status_code=status.HTTP_200_OK,
    summary="Show extracted information by Id."
)
async def get_extracted_information(
    document_id: str
):
    """
    """
    try:
        extracted_data = db_judicatura.search_document_by_id(
            field="_id", key=ObjectId(document_id))

        if not isinstance(extracted_data, ExtractedResponse):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=f"{extracted_data}")

        return extracted_data

    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)


@router.post(
    path="/search",
    response_model=SearchResponse,
    status_code=status.HTTP_202_ACCEPTED,
    summary="Realizar consulta por documento."
)
async def post_send_notification(
    data: SearchRequest,
    background_tasks: BackgroundTasks
):
    """
    """
    try:
        background_tasks.add_task(
            write_notification, data.document)
        return {"msg": "Se recibe la solicitud correctamente."}
    except Exception as error:
        logging.error(error)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=error)
