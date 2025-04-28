from typing import Dict, List, Optional, Any, Union

from google.genai import Client
from config import GEMINI_API_KEY, GEMINI_MODEL
from modules.prompt_manager import PromptManager


class AIProcessor:
    def __init__(self):
        self.client = Client(api_key=GEMINI_API_KEY)
        self.prompt = PromptManager()
        self.conversation_history: List[Dict[str, str]] = []

    def _add_to_history(self, role: str, content: str) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def ask_ai(self, prompt: str, image_path: Optional[str] = None) -> Optional[str]:
        """Ask Gemini a question with optional image input."""
        try:
            if image_path:
                with open(image_path, "rb") as image_file:
                    file = self.client.files.upload(
                        file=image_file, config={"mime_type": "image/png"}
                    )

                # Generate response with Image
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=[file, prompt],
                )
            else:
                # Generate response without Image
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=prompt,
                )

            # Add to conversation history
            self._add_to_history("user", prompt)
            if response.text:
                self._add_to_history("model", response.text)

            return response.text
        except Exception as e:
            print(f"Error communicating with Gemini: {e}")
            return None

    def get_history(self):
        return self.conversation_history
