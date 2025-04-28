import json
from typing import Dict, Any


class PromptManager:
    def get_content_extraction_prompt(self) -> str:
        return """
            Extract all the text from this old article image.
            Return only the extracted text without any additional commentary.
            Preserve paragraph breaks and structural elements as much as possible.
        """

    def get_combined_prompt(
        self,
        extracted_text: str,
        xml_metadata: Dict[str, Any],
        response_template: str,
    ) -> str:
        return f"""
            You are tasked with structuring historical news article content into a strict JSON format by intelligently analyzing extracted OCR text and XML metadata.

            Sources:
            - Extracted Text (may contain OCR or spelling errors):
            ```
            {extracted_text}
            ```

            - XML Metadata:
            ```
            {xml_metadata}
            ```

            JSON Response Structure (strict structure to follow):
            {response_template}

            Instructions:
            1. Thoroughly analyze both the extracted text and XML metadata.
            2. Reconcile discrepancies between the two sources:
            - Prefer XML metadata if confidence is high.
            - Correct OCR/spelling errors in extracted text while maintaining meaning.
            - Standardize proper nouns (names, locations) and dates accurately.
            3. Populate ALL fields in the JSON template:
            - Use inference when data is missing (based on context).
            - If a field cannot be reliably determined, use `null`.
            4. For the "content" field:
            - Divide the article into logical paragraphs.
            - Correct grammar, spelling, and flow while preserving historical context.
            5. In the "metadata" section:
            - Note any major corrections, reconciliations, or uncertainties.
            6. Ensure all numbers, dates, and units are accurately formatted.
            7. Maintain only plain text (no HTML tags, styling, or formatting codes).

            Output Requirements:
            - Return ONLY a raw JSON object that strictly follows the provided template.
            - No explanations, code blocks, markdown, or additional text.
            - The response must begin with '{{' and end with '}}'.
            - Ensure the JSON is valid, properly formatted, and ready for programmatic parsing.

            Strict adherence to formatting is critical, as this JSON will be automatically processed.
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
