import json
from google.genai import Client
import xml.etree.ElementTree as ET
from modules.data_saver import DataSaver
from config import GEMINI_API_KEY, GEMINI_MODEL


class ArticleProcessingAgent:
    """An agentic approach to processing old article images and metadata."""

    def __init__(self):
        self.client = Client(api_key=GEMINI_API_KEY)
        self.conversation_history = []
        self.extracted_data = {}
        self.data_saver = DataSaver()

    def _add_to_history(self, role, content):
        """Add a message to the conversation history."""
        self.conversation_history.append({"role": role, "content": content})

    def _ask_gemini(self, prompt, image_path=None):
        """Ask Gemini a question with optional image input."""
        try:
            if image_path:
                with open(image_path, "rb") as image_file:
                    file = self.client.files.upload(file=image_file, config={
                        "mime_type": "image/png"
                    })

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
            self._add_to_history("model", response.text)

            return response.text
        except Exception as e:
            print(f"Error communicating with Gemini: {e}")
            return None

    def _parse_element(self, element):
        """Recursively parse an XML element and its children."""
        result = {}

        # If the element has children
        if len(element) > 0:
            children_data = {}
            for child in element:
                child_data = self._parse_element(child)

                # Handle the child's data
                if child.tag in children_data:
                    # If this tag already exists, convert to list or append
                    if not isinstance(children_data[child.tag], list):
                        children_data[child.tag] = [children_data[child.tag]]
                    if isinstance(child_data[child.tag], list):
                        # If child_data is already a list, extend it
                        children_data[child.tag].extend(child_data[child.tag])
                    else:
                        # If child_data is not a list, append it
                        children_data[child.tag].append(child_data[child.tag])
                else:
                    # First occurrence of this tag
                    children_data[child.tag] = child_data[child.tag]

            result[element.tag] = children_data
        else:
            # Element has no children, just text
            result[element.tag] = element.text.strip() if element.text else ""

        return result

    def extract_text_from_image(self, image_path):
        """Extract all text from the article image."""
        prompt = """
        I'm processing an old article image. Please extract ALL text visible in this image.
        Include the title, author, date, and complete article text.
        Preserve paragraph structure. Format the output clearly.
        """

        result = self._ask_gemini(prompt, image_path=image_path)
        self.extracted_data["raw_image_text"] = result
        return result

    def parse_xml_metadata(self, xml_path):
        """Parse the XML metadata file and extract structured information with any level of nesting."""
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            # Use a recursive function to handle elements at any nesting level
            metadata = self._parse_element(root)

            # Since we want the root element's children as the top level, not the root itself
            if (
                isinstance(metadata, dict)
                and len(metadata) == 1
                and root.tag in metadata
            ):
                metadata = metadata[root.tag]

            self.extracted_data["xml_metadata"] = metadata
            return metadata
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return {}

    def compare_sources(self):
        """Compare the extracted text with XML metadata and identify discrepancies."""
        if not self.extracted_data.get("raw_image_text") or not self.extracted_data.get(
            "xml_metadata"
        ):
            return "Error: Missing extracted text or XML metadata. Run extraction steps first."

        prompt = f"""
        I need to compare the text extracted from an image with metadata from an XML file.
        
        EXTRACTED TEXT FROM IMAGE:
        ```
        {self.extracted_data["raw_image_text"]}
        ```
        
        XML METADATA:
        ```
        {json.dumps(self.extracted_data["xml_metadata"], indent=2)}
        ```
        
        Please:
        1. Identify any discrepancies between these two sources
        2. Determine which source is likely more accurate for each discrepancy
        3. Provide a confidence score (0-100%) for each determination
        4. Return the analysis in a structured format
        """

        result = self._ask_gemini(prompt)
        self.extracted_data["comparison_analysis"] = result
        return result

    def structure_content(self, response_template):
        """Structure the extracted content according to the provided template."""
        if not self.extracted_data.get("raw_image_text"):
            return "Error: Missing extracted text. Run extraction step first."

        prompt = f"""
        Based on the article text I extracted and our analysis, please structure the content 
        according to this JSON template:
        
        {json.dumps(response_template, indent=2)}
        
        EXTRACTED TEXT:
        ```
        {self.extracted_data["raw_image_text"]}
        ```
        
        XML METADATA (for reference):
        ```
        {json.dumps(self.extracted_data.get("xml_metadata", {}), indent=2)}
        ```
        
        COMPARISON ANALYSIS (for reference):
        ```
        {self.extracted_data.get("comparison_analysis", "Not available")}
        ```
        
        Please:
        1. Fill in all fields in the template based on the available information
        2. For the "content" field, break down the article into logical paragraphs
        3. Include any relevant metadata about discrepancies in the "metadata" field
        4. Return ONLY valid JSON that matches the template structure
        """

        result = self._ask_gemini(prompt)

        if result:
            # Try to extract JSON from the response
            try:
                # Find JSON pattern in the response
                start_idx = result.find("{")
                end_idx = result.rfind("}") + 1

                if start_idx >= 0 and end_idx > start_idx:
                    json_str = result[start_idx:end_idx]
                    structured_result = json.loads(json_str)
                    self.extracted_data["structured_result"] = structured_result
                    return structured_result
                else:
                    return {
                        "error": "Could not extract JSON from response",
                        "raw_response": result,
                    }
            except json.JSONDecodeError:
                return {"error": "Invalid JSON in response", "raw_response": result}
        else:
            return result

    def generate_html(self):
        """Generate HTML representation of the article."""
        if not self.extracted_data.get("structured_result"):
            return "Error: Missing structured result. Run structure_content step first."

        prompt = f"""
        Create a clean, well-formatted HTML page for the article with the following content:
        
        {json.dumps(self.extracted_data["structured_result"], indent=2)}
        
        Requirements:
        1. Use semantic HTML5 tags
        2. Include basic responsive styling
        3. Make it printer-friendly
        4. Use a clean, readable design appropriate for an academic/historical article
        5. Return ONLY the complete HTML code, including <html>, <head>, and <body> tags
        """

        result = self._ask_gemini(prompt)

        if result:
            # Try to extract HTML from response
            html_start = result.find("<html")
            html_end = result.rfind("</html>") + 7

            if html_start >= 0 and html_end > html_start:
                html_code = result[html_start:html_end]
                self.extracted_data["html_content"] = html_code
                return html_code
            else:
                return result  # Return the full response if we couldn't extract HTML
        else:
            return result

    def process_article(self, image_path, xml_path, response_template):
        """Complete end-to-end processing of an article."""
        # Step 1: Extract text from image
        print("Step 1: Extracting text from image...")
        self.extract_text_from_image(image_path)

        # Step 2: Parse XML metadata
        print("Step 2: Parsing XML metadata...")
        self.parse_xml_metadata(xml_path)

        # Step 3: Compare sources
        print("Step 3: Comparing sources...")
        self.compare_sources()

        # Step 4: Structure content
        print("Step 4: Structuring content...")
        structured_content = self.structure_content(response_template)

        # Step 5: Generate HTML
        print("Step 5: Generating HTML...")
        html_content = self.generate_html()

        # Return results
        return {
            "structured_content": structured_content,
            "html_content": html_content,
            "all_data": self.extracted_data,
        }

    def save_results(self, output_dir):
        self.data_saver.save_processing_data(output_dir, self.extracted_data)
