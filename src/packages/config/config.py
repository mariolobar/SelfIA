import os

class Config:

    """
    Holds configuration settings for Azure services used within the application.

    This class initializes and provides access to configuration variables related to
    Azure Services.
    
    """

    def __init__(self) -> None:

        """
        Initializes configuration settings for use throughout the application.
        """

        # OpenAI


        self.config_openai_key = "DnW2xDeKi4aEcyUWpTM4ECXedEJ1JVTsNA3fYScrDS0uZtqPAQUEJQQJ99AJACYeBjFXJ3w3AAABACOGNFaL"
        self.config_openai_api_version = "2024-02-01"
        self.config_openai_api_base = "https://openai-poc-selfia.openai.azure.com/"
        self.config_openai_deployment_gpt = "gpt-4"
        self.config_openai_deployment_dalle = "dall-e-3"
        self.config_openai_deployment_gpt_4o  = "gpt-4o"


        # Storage Account
        self.config_storage_account_name = "storagepocselfi"
        self.config_storage_account_key = "GRU1at5Wyo2PDMbHACgrWAhcThR1y6rdhEyxjpxPVUw59QgQuPsaSH3mz9KOXl7Px1vnC67M6Tuw+ASt+662UA=="
        self.config_storage_account_ip_container = "poc-input-selfi"
        self.config_storage_account_op_container = "poc-generated-selfi"