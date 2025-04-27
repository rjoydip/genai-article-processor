from google.genai import types, Client
from config import GEMINI_API_KEY, GEMINI_MODEL, RESPONSE_STRUCTURE


class AIProcessor:
    def __init__(self):
        self.client = Client(api_key=GEMINI_API_KEY)

    def compare_and_process(self, extracted_text, xml_metadata, xml_content_sections):
        """Compare extracted text with XML metadata and generate structured response."""
        try:
            # Construct the prompt for Gemini
            prompt = f"""
            I have an old article from which I've extracted text and XML metadata.
            
            EXTRACTED TEXT FROM IMAGE:
            ```
            {extracted_text}
            ```

            XML METADATA:
            ```
            {xml_metadata}
            ```

            XML CONTENT SECTIONS:
            ```
            {xml_content_sections}
            ```

            Please analyze both sources and:
            1. Verify if the XML metadata matches information found in the extracted text
            2. Identify any discrepancies between the two sources
            3. Create a comprehensive structured response with the following JSON structure:
            {RESPONSE_STRUCTURE}

            For the content field, divide the article into logical paragraphs.
            For any fields where XML and extracted text disagree, note this in the metadata section.

            IMPORTANT: Return ONLY the raw JSON object without any markdown formatting, code blocks, or explanations. The response must begin with the opening curly brace '{' and end with the closing curly brace '}' with no additional characters.
            """

            # Generate content using the updated API
            response = self.client.models.generate_content(
                model=GEMINI_MODEL,
                contents=prompt,
            )

            if response.text:
                return response.text.replace("```json", "").replace("```", "")
            else:
                print("Empty response text")
                return None
        except Exception as e:
            print(f"Error in AI processing: {e}")
            return None
