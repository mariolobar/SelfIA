import azure.functions as func
import json
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    # Define available filters with name, description, and status
    filters = [
        {"name": "FunkoMe", "description": "Creates a Funko-style version", "status": True},
        {"name": "SnapHero", "description": "Transform the photo into a vibrant superhero character", "status": True},
        {"name": "MyPixar", "description": "Pixar-style animated filter", "status": True},

    ]
    
    response = {
        "filters": filters
    }

    logging.info(json.dumps(response))
    
    # Return JSON response
    return func.HttpResponse(
        json.dumps(response),
        status_code=200
    )