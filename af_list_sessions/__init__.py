import logging
from src.packages.managers.storage_manager import AzureStorageManager
import azure.functions as func
import json


def main(req: func.HttpRequest) -> func.HttpResponse:

    storage_manager = AzureStorageManager()

    mortgages_list = storage_manager.list_blobs_with_metadata(container_name = "poc-input-selfi")

    response_body = json.dumps(mortgages_list)

    return func.HttpResponse(
            response_body,
            status_code=200
    )
