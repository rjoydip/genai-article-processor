import asyncio
from functools import partial
from typing import Dict, List, Optional

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

    def _upload_file(self, image_path: str):
        """Helper method to upload a file - runs in executor."""
        with open(image_path, "rb") as image_file:
            return self.client.files.upload(
                file=image_file, config={"mime_type": "image/png"}
            )

    async def ask_ai(
        self, prompt: str, image_path: Optional[str] = None
    ) -> Optional[str]:
        """Ask Gemini a question with optional image input."""
        try:
            loop = asyncio.get_event_loop()
            if image_path:
                # Use loop.run_in_executor for file operations
                upload_func = partial(self._upload_file, image_path)
                file = await loop.run_in_executor(None, upload_func)

                # Generate response with Image - run API call in executor
                response_func = partial(
                    self.client.models.generate_content,
                    model=GEMINI_MODEL,
                    contents=[file, prompt],
                )
                response = await loop.run_in_executor(None, response_func)
            else:
                # Generate response without Image
                response_func = partial(
                    self.client.models.generate_content,
                    model=GEMINI_MODEL,
                    contents=prompt,
                )
                response = await loop.run_in_executor(None, response_func)

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
