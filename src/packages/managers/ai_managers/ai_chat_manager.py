"""
Provides AIChatManager class to interact with Azure OpenAI
"""
from typing import List, Dict
import copy
from openai import AzureOpenAI

from src.packages.config.config import Config


class AIChatManager:
    """
    Manages interactions with Azure OpenAI, including creating system prompts,
    sending chat completion requests, and updating chat histories.

    Attributes
    ----------
    config : Config
        Configuration settings for the AIChatManager.
    openai_deployment_gpt : str
        Deployment name of the OpenAI GPT model.
    client : AzureOpenAI
        Client for interacting with the Azure OpenAI API.

    Methods
    -------
    get_response_openai(complete_chat: List[Dict[str, str]], temperature: float = 0) -> str
        Sends a chat completion request to the OpenAI API and returns the response.
    """

    def __init__(self) -> None:
        """
        Initializes the AIChatManager with configuration settings and Key Vault client.
        """

        # Init config
        self.config = Config()

        # Initialize OpenAI
        self.openai_deployment_gpt = self.config.config_openai_deployment_gpt

        # Create AzureOpenAI client
        self.client = AzureOpenAI(
            azure_endpoint=self.config.config_openai_api_base,
            api_key=self.config.config_openai_key,
            api_version=self.config.config_openai_api_version
        )

    def get_response_openai(
        self,
        complete_chat: List[Dict[str, str]],
        temperature: float = 0
    ) -> str:
        """
        Sends a chat completion request to the OpenAI API and returns the response.

        Parameters:
        -------
        complete_chat (List[Dict[str, str]]):
        The chat history including user and assistant messages.
        temperature (float): The sampling temperature to use.
        Higher values make the output more random.

        Returns:
        -------
        str: The response content from the OpenAI API.
        """
        response = self.client.chat.completions.create(
            model=self.openai_deployment_gpt,
            messages=complete_chat,
            temperature=temperature
        )

        response_content = response.choices[0].message.content.strip()
        return response_content
    
    def update_system_message(
        self,
        complete_chat: List[Dict[str, str]],
        input_text: str
    ) -> List[Dict[str, str]]:
        """
        Updates the system message in the chat history. If a system message exists, it is updated.

        Parameters:
        -------
        complete_chat (List[Dict[str, str]]):
        The chat history including user and assistant messages.
        input_text (str):
        Context to be added.

        Returns:
        -------
        List[Dict[str, str]]: The updated chat history with the system message.
        """
        complete_chat_copy = copy.deepcopy(complete_chat)
        if len(complete_chat_copy) != 0:
            has_system_message = False
            ind_dict = 0
            while (ind_dict < len(complete_chat_copy)) and (not has_system_message):
                if complete_chat_copy[ind_dict]['role'] == 'system':
                    complete_chat_copy[ind_dict]['content'] = complete_chat_copy[ind_dict]['content'].replace("[REPLACE_CONTEXT]",str(input_text))
                    has_system_message = True
                ind_dict += 1

            if not has_system_message:

                raise Exception("Chat log must contain at least the system information")

        else:

            raise Exception("Chat log must contain at least the system information")

        return complete_chat_copy
    