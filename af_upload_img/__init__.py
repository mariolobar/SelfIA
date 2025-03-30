import logging
import uuid
import json
import azure.functions as func
from src.packages.managers.storage_manager import AzureStorageManager
import base64


def main(req: func.HttpRequest) -> func.HttpResponse:

        storage_manager = AzureStorageManager()
        req_body = req.get_json()
        file_content = req_body.get("upload_file")
        blob_name = "img.png"
        #     blob_name = file_content.filename

        # Elimina el encabezado, si existe
        if file_content.startswith("data:"):
            file_content = file_content.split(",")[1]

        # Asegúrate de que el padding sea correcto
        missing_padding = len(file_content) % 4
        if missing_padding:
            file_content += '=' * (4 - missing_padding)

        # Decodifica la imagen Base64
        file_data = base64.b64decode(file_content)

        session_id = str(uuid.uuid4())
        extension = blob_name.split(".")[-1]
        metadata = {"file_name":blob_name.split(".")[0]}
        storage_manager.upload_blob(container_name="poc-input-selfi", blob=session_id + "." + extension, data=file_data, metadata = metadata)

        return_dict = {"session_id":session_id,
                        "stored_img":session_id + "." + extension}

        return func.HttpResponse(
                json.dumps(return_dict),
                status_code=200
        )
