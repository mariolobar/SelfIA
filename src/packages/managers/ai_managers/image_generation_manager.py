"""
Provides ImageGenerationManager class to interact with Azure OpenAI and generate selfi images
"""
import logging
import json
from openai import AzureOpenAI

from src.packages.config.config import Config

class ImageGenerationManager:
    """
    Manages image generation using DALL-E 3 in Azure OpenAI, including generating images
    with specific filters and creating image descriptions.
    
    Attributes
    ----------
    client : AzureOpenAI
        Azure OpenAI client configured with the API key and endpoint.
        
    Methods
    -------
    generate_image_with_dalle3(image_description: str, filter_name: str) -> str
        Generates a stylized image based on a description and filter.
    generate_image_description(blob_image_url: str) -> str
        Creates a description of an image using Azure OpenAI's GPT model.
    """

    def __init__(self):
        """
        Initializes the ImageGenerationManager instance with configuration settings
        and the Azure OpenAI client.
        """
        # Load configuration
        self.config = Config()
        
        # Initialize OpenAI
        self.openai_deployment_gpt_4o = self.config.config_openai_deployment_gpt_4o
        self.openai_deployment_dalle = self.config.config_openai_deployment_dalle

        self.client = AzureOpenAI(
            api_version="2024-05-01-preview",
            azure_endpoint=self.config.config_openai_api_base,  
            api_key=self.config.config_openai_key
        )

    def generate_image_with_dalle3(self, image_description: str, filter_name: str) -> str:
        """
        Generates an image based on the provided description and filter name using DALL-E 3.

        Parameters
        ----------
        image_description : str
            Description of the image content, including details like gender, hairstyle, etc.
        filter_name : str
            The name of the filter style to apply, e.g., 'FunkoMe', 'SnapHero', 'MyPixar'.

        Returns
        -------
        str
            URL of the generated image.
        
        Raises
        ------
        Exception
            If an error occurs during image generation.
        """
        # Define prompt based on selected filter
        base_prompt = image_description + f" transform it into a {filter_name}-style image. Ensure that the transformed character retains their gender, hairstyle, clothing, and overall likeness, including facial features and expression."
        
        # Customize prompt for specific filters
        if filter_name == "FunkoMe":
            prompt = base_prompt + (
            "Transform the person in this image into a FunkoMe figure. "
            "The character should maintain the features and expression from the original photo, "
            "with bright colors and a playful vibe, resembling the distinctive FunkoPop style."
        )
        elif filter_name == "SnapHero":
             prompt = base_prompt + (
            "Transform the person in this image into a vibrant superhero character. "
            "Create a cartoon-style portrait featuring bold outlines and exaggerated features. "
            "The superhero should have a dynamic pose, showcasing strength and confidence. "
            "Incorporate bright, vibrant colors in their costume and background to enhance the heroic theme. "
            "Ensure the character retains the original person's gender, hairstyle, and key facial features while embodying the essence of a superhero."
        )
        elif filter_name == "MyPixar":
            prompt = base_prompt + (
            "Create a Pixar-style character portrait of the person in this image. "
            "The character should have large, expressive eyes that convey emotion, and the lighting should be soft and warm, enhancing the friendly atmosphere. "
            "Use smooth textures for the skin and clothing to mimic the polished look of Pixar animation. "
            "Ensure the character retains the original person's hairstyle, gender, and distinct facial features, capturing their essence in a whimsical, cinematic style."
        )
        else:
            prompt = base_prompt + "Create a stylized portrait of the person in this image, with a unique artistic filter applied."

        # Generate image with DALL-E 3
        try:
            result = self.client.images.generate(
                model= self.openai_deployment_dalle,
                prompt=prompt,
                n=1
            )
            generated_image_url = json.loads(result.model_dump_json())['data'][0]['url']
            return generated_image_url
        except Exception as e:
            raise Exception(f"Error generating image with DALL-E 3: {e}")

    def generate_image_description(self, blob_image_url: str) -> str:
        """
        Generates a detailed description of an image from the provided Blob URL.

        Parameters
        ----------
        blob_image_url : str
            URL of the image stored in Azure Blob Storage.

        Returns
        -------
        str
            Description of the image content generated by Azure OpenAI.
        
        Raises
        ------
        Exception
            If an error occurs during description generation.
        """
        try:
            response = self.client.chat.completions.create(
                model= self.openai_deployment_gpt_4o,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": "Analyze this image and provide a detailed description about the gender, hairstyle, clothing, and overall likeness, including facial features and expression."},
                            {"type": "image_url", "image_url": {"url": blob_image_url}},
                        ],
                    }
                ],
                max_tokens=300,
            )
            
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating image description: {e}")
