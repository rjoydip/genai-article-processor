import json
from typing import Dict, Any

from config import RESPONSE_STRUCTURE


class PromptManager:
    def get_content_extraction_prompt(self) -> str:
        return """
            Extract all the text from this old article image.
            Return only the extracted text without any additional commentary.
            Preserve paragraph breaks and structural elements as much as possible.
        """

    def get_combined_prompt(
        self, extracted_text: str, xml_metadata: Dict[str, Any]
    ) -> str:
        return f"""
            I have an old article from which I've extracted text and XML metadata. I need you to analyze both, reconcile any differences, and generate a complete structured JSON response according to the specified format.

            EXTRACTED TEXT FROM IMAGE:
            ```
            {extracted_text}
            ```

            XML METADATA:
            ```
            {xml_metadata}
            ```

            Instructions:
            1. Analyze both the extracted text and XML metadata thoroughly
            2. Identify and reconcile any discrepancies between these sources
            3. For missing properties in either source, make reasonable inferences based on available information
            4. If a property cannot be reliably determined, use null or provide a best guess with a confidence indicator
            5. Ensure all required fields in the response structure are populated
            6. For the content field, divide the article into logical paragraphs
            7. Note any discrepancies between sources in the metadata section

            Required JSON Response Structure:
            {RESPONSE_STRUCTURE}

            OUTPUT REQUIREMENTS:
            - Return ONLY a raw JSON object with no explanations or markdown formatting
            - The response must begin with '{" and end with "}'
            - Ensure the JSON is valid and properly formatted
            - Include ALL fields specified in the response structure
            - For any missing values that cannot be determined, use null or a reasonable inference
            - Do not add any text before or after the JSON object

            This response will be programmatically parsed, so strict adherence to these formatting requirements is essential.
        """

    def get_structure_content_prompt(
        self,
        response_template: Dict[str, Any],
        raw_image_text: str,
        xml_metadata: Dict[str, Any],
        combined_content: Any,
    ) -> str:
        return f"""
            I need you to structure the following news article content according to a specific JSON template, while correcting any spelling or OCR errors in the text.

            JSON TEMPLATE:
            {json.dumps(response_template, indent=2)}

            EXTRACTED TEXT (may contain OCR errors):
            ```
            {raw_image_text}
            ```

            XML METADATA (for reference):
            ```
            {xml_metadata}
            ```

            COMBINED ANALYSIS (for reference):
            ```
            {combined_content}
            ```

            INSTRUCTIONS:
            1. Fill in ALL fields in the template using the available information
            2. Correct any spelling mistakes or OCR errors in the text while preserving the original meaning
            3. For the "content" field, divide the article into logical paragraphs while maintaining the original flow
            4. Standardize proper nouns, names, and places with correct spelling and formatting
            5. Ensure dates, numbers, and measurements are accurately represented
            6. In the "metadata" field, document any significant corrections made or discrepancies found
            7. If information for a field is truly unavailable, use null but attempt to infer missing information when possible
            8. Generate plain text only - no HTML styling, no images, no formatting tags

            OUTPUT REQUIREMENTS:
            - Return ONLY a valid JSON object that precisely follows the template structure
            - Do not include any explanations, code blocks, or additional text
            - Ensure the response begins with '{" and ends with "}'
            - Format all text properties with proper capitalization, punctuation, and spacing
            - Preserve the historical context and terminology of the original text
            - Include only plain text content without any HTML elements, styling, or images

            This JSON will be programmatically processed, so strict adherence to the template structure is critical.
        """

    def get_html_prompt(self, structured_content: Dict[str, Any]) -> str:
        return f"""
            Create a clean, text-only HTML page for the article with the following content:

            {json.dumps(structured_content, indent=2)}

            Requirements:
            1. Use semantic HTML5 tags (like article, header, section, p)
            2. NO CSS styling - return only structural HTML
            3. NO images or other media elements
            4. Use simple, semantic document structure appropriate for an academic/historical article
            5. Include proper metadata in the head section
            6. Focus on content readability and semantic structure only
            7. Return ONLY the complete HTML code, including <!DOCTYPE html>, <html>, <head>, and <body> tags

            The output should be valid HTML5 focused solely on content structure without any visual styling.
        """
