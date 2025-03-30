"""
Provides manager to handle the AI Services
"""

from src.packages.config.config import Config
from src.packages.managers.ai_managers.ai_chat_manager import AIChatManager
from src.packages.managers.ai_managers.image_generation_manager import ImageGenerationManager

class AIManager:

    """Manager to handle the AI Services"""

    def __init__(self) -> None:

        """
        Initializes variables to be used by the class.
        """

        # Initialize Config file
        self.config = Config()

        # Initialize AIChatManager
        self.ai_chat_manager = AIChatManager()

        # Initialize AISearchManager
        self.image_generation_manager  =ImageGenerationManager()

