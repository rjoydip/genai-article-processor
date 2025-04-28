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

    def get_compare_prompt(self, extracted_text: str, xml_metadata: Dict[str, Any], xml_content_sections: Any) -> str:
        return f"""
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

    def get_structure_content_prompt(
        self, response_template: Dict[str, Any], raw_image_text: str, xml_metadata: Dict[str, Any], comparison_analysis: Any
    ) -> str:
        return f"""
            Based on the article text I extracted and our analysis, please structure the content 
            according to this JSON template:

            {json.dumps(response_template, indent=2)}

            EXTRACTED TEXT:
            ```
            {raw_image_text}
            ```

            XML METADATA (for reference):
            ```
            {json.dumps(xml_metadata, indent=2)}
            ```

            COMPARISON ANALYSIS (for reference):
            ```
            {comparison_analysis}
            ```

            Please:
            1. Fill in all fields in the template based on the available information
            2. For the "content" field, break down the article into logical paragraphs
            3. Include any relevant metadata about discrepancies in the "metadata" field
            4. Return ONLY valid JSON that matches the template structure
        """

    def get_html_prompt(self, structured_result: Dict[str, Any]) -> str:
        return f"""
            Create a clean, well-formatted HTML page for the article with the following content:
            
            {json.dumps(structured_result, indent=2)}
            
            Requirements:
            1. Use semantic HTML5 tags
            2. Include basic responsive styling
            3. Make it printer-friendly
            4. Use a clean, readable design appropriate for an academic/historical article
            5. Return ONLY the complete HTML code, including <html>, <head>, and <body> tags
        """
