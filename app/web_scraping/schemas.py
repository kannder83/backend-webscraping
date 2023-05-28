

def document_schema(document) -> dict:
    return {
        "id": str(document["_id"]),
        "documento": document["documento"],
        "fecha_creacion": document["fecha_creacion"],
        "procesos": document["procesos"],
    }


def documents_schema(documents) -> list:
    return [document_schema(document) for document in documents]


def aggregate_schema(document) -> dict:
    serialized_document = {
        "id": str(document["_id"]),
        "documento": document["documento"],
        "fecha_creacion": document["fecha_creacion"],
        "cantidad_procesos": document["cantidad_procesos"],
    }
    return serialized_document


def aggregates_schema(documents) -> list:
    serialized_documents = [aggregate_schema(
        document) for document in documents]
    return serialized_documents
