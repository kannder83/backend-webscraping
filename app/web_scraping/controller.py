import logging
from app.web_scraping.schemas import document_schema, aggregates_schema, aggregate_schema
from config.database import db_client
from app.web_scraping.models import ExtractedResponse, ExtractedResumeResponse


class DbJudicatura():
    """
    """

    def __init__(self):
        self.judicatura_collection = db_client.judicatura

    def search_document_by_id(self, field: str, key) -> any:
        """
        """
        try:
            logging.info(f"DB >>> Field: {field} key: {key}")

            proceso = document_schema(
                self.judicatura_collection.find_one({field: key}))

            if not proceso:
                raise "Proceso sin datos."

            return ExtractedResponse(**proceso)

        except Exception as error:
            logging.error(error)
            return f"{error}"

    def get_store_ids(self) -> any:
        """
        """
        get_all_ids: list = []
        try:
            pipeline = [
                {
                    "$match": {}
                },
                {
                    "$project": {
                        "_id": 1,
                        "documento": 1,
                        "fecha_creacion": 1,
                        "cantidad_procesos": {
                            "$reduce": {
                                "input": "$procesos",
                                "initialValue": 0,
                                "in": {
                                    "$sum": [
                                        "$$value",
                                        {"$size": "$$this"}
                                    ]
                                }
                            }
                        }
                    }
                }
            ]

            result = self.judicatura_collection.aggregate(pipeline)

            for document in result:
                get_all_ids.append(document)

            logging.info(f"AGGREGATE >>> {get_all_ids}")

            data = aggregates_schema(get_all_ids)

            logging.info(f"AGGREGATE DATA >>> {data}")

            return data

        except Exception as error:
            logging.error(error)
            return f"{error}"


db_judicatura = DbJudicatura()
