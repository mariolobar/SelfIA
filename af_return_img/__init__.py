import logging
from src.packages.managers.storage_manager import AzureStorageManager
import azure.functions as func
import base64
import json


def main(req: func.HttpRequest) -> func.HttpResponse:

    req_body = req.get_json()
    image_id = req_body.get("image_id")

    storage_manager = AzureStorageManager()

    img_data = storage_manager.get_blob(container_name="poc-generated-selfi", blob=image_id, fmt="img")
    img_bytes = img_data.read()

    img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    response_dict = {"base64_img": "data:image/png;base64," + img_base64}

    return func.HttpResponse(
            body=json.dumps(response_dict),
            mimetype="application/json",
            status_code=200
        )
