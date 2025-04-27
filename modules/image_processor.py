from google.genai import Client
from config import GEMINI_API_KEY, GEMINI_MODEL


class ImageProcessor:
    def __init__(self):
        self.client = Client(api_key=GEMINI_API_KEY)

    def extract_text_from_image(self, image_path):
        """Extract text from the article image using Gemini."""
        try:
            # Open and prepare image
            with open(image_path, "rb") as image_file:
                # Prompt for text extraction
                prompt = """
                Extract all the text from this old article image. 
                Return only the extracted text without any additional commentary.
                Preserve paragraph breaks and structural elements as much as possible.
                """

                file = self.client.files.upload(file=image_file, config={
                    "mime_type": "image/png"
                })

                # Generate content using the updated API
                response = self.client.models.generate_content(
                    model=GEMINI_MODEL,
                    contents=[file, prompt],
                )

                self.client.files.delete(name=file.name) # type: ignore

                return response.text
        except Exception as e:
            print(f"Error extracting text from image: {e}")
            return None
