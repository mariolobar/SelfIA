import requests
import json
import logging
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
from src.packages.managers.ai_managers.ai_manager import AIManager
from src.packages.managers.storage_manager import AzureStorageManager


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Processing file with selected filters.')

    try:
        
        # Parse request body
        req_body = req.get_json()
        container_name = req_body.get('container_name',"poc-input-selfi")
        session_id = req_body.get('session_id')
        blob_filename = req_body.get('stored_img')
        filters = req_body.get('filters')

        # Initialize AIManager
        ai_manager = AIManager()
        image_generation_manager = ai_manager.image_generation_manager
        storage_manager = AzureStorageManager()

        # Validate input parameters
        if not session_id:
            return func.HttpResponse("No session_id provided.", status_code=400)
        
        if not blob_filename:
            return func.HttpResponse(json.dumps({"status": "400 Bad Request", "message": "No stored_img provided."}), status_code=400)

        if not filters:
            return func.HttpResponse("No filters provided.", status_code=400)
      
        # Generate the image URL from Blob Storage using StorageManager
        blob_image_url = storage_manager.get_blob_url_with_sas(container_name, blob_filename)
        logging.info(f"Blob image URL with SAS: {blob_image_url}")
        
        # Generate description using GPT-4o from ImageGenerationManager
        image_description = image_generation_manager.generate_image_description(blob_image_url)
        logging.info(f"Image description of input image: {image_description}")

        generated_images = {}
        
        # Generate images for each selected filter
        for filter_name in filters:
            try:
                generated_image_url = image_generation_manager.generate_image_with_dalle3(image_description, filter_name)
                generated_images[filter_name] = generated_image_url
        
                # Save each generated image in a session-specific folder
                output_container_name = "poc-generated-selfi"
                output_blob_name = f"{session_id}/{session_id}_{filter_name}.png"
                image_content = requests.get(generated_image_url).content
                storage_manager.upload_blob(output_container_name, output_blob_name, image_content)
                logging.info(f"Stored generated image for filter '{filter_name}' at blob: {output_blob_name}")
                # Store image path in response
                generated_images[filter_name] = storage_manager.get_blob_url_with_sas(output_container_name, output_blob_name)

            except Exception as e:
                logging.error(f"Error generating image for filter '{filter_name}': {str(e)}")
                generated_images[filter_name] = {"error": str(e)}
            
        # Build response
        response = {
            "status": "200 OK",
            "message": "Images generated successfully.",
            "files": generated_images
        }

        logging.info(response)
        
        return func.HttpResponse(json.dumps(response), status_code=200)

    except ValueError as e:
        return func.HttpResponse(json.dumps({"status": "400 Bad Request", "message": str(e)}),status_code=400)
    except ResourceNotFoundError:
        return func.HttpResponse(json.dumps({"status": "404 Not Found", "message": "Blob not found."}),status_code=404)
    except Exception as e:
        logging.error(f"Error processing request: {str(e)}")
        return func.HttpResponse(json.dumps({"status": "500 Internal Server Error", "message": "Internal server error."}),status_code=500)