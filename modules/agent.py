from typing import Dict, Any

from google.genai import Client
from config import GEMINI_API_KEY
from modules.ai_processor import AIProcessor
from modules.data_saver import DataSaver
from modules.html_processor import HTMLProcessor
from modules.prompt_manager import PromptManager
from utils import UtilityManager
from modules.xml_parser import XMLParser


class ArticleProcessorAgent:
    """An agentic approach to processing old article images and metadata."""

    def __init__(self):
        self.client = Client(api_key=GEMINI_API_KEY)
        self.data_saver = DataSaver()
        self.prompt = PromptManager()
        self.ai_processor = AIProcessor()
        self.html_processor = HTMLProcessor()
        self.utility_manager = UtilityManager()
        self.xml_parser = XMLParser()
        self.extracted_data: Dict[str, Any] = {}

    def process_article(self, image_path: str, xml_path: str, response_template: Dict[str, Any], output_path: str) -> Dict[str, Any]:
        """Complete end-to-end processing of an article."""
        # Step 1: Extract text from image
        print("Step 1: Extracting text from image...")
        self.extracted_data["raw_image_text"] = self.ai_processor.ask_gemini(
            self.prompt.get_content_extraction_prompt(), image_path
        )

        # Step 2: Parse XML metadata
        print("Step 2: Parsing XML metadata...")
        self.extracted_data["xml_metadata"] = self.xml_parser.parse_xml_metadata(
            xml_path
        )

        # Step 3: Compare sources
        print("Step 3: Comparing content...")
        comparison_analysis = self.ai_processor.ask_gemini(
            self.prompt.get_compare_prompt(
                self.extracted_data.get("raw_image_text", ""),
                self.extracted_data.get("xml_metadata", ""),
                self.extracted_data.get("xml_metadata", ""),
            )
        )

        self.extracted_data["comparison_analysis"] = (
            self.utility_manager.structure_json(comparison_analysis)
        )

        # Step 4: Structure content
        print("Step 4: Structuring content...")
        structured_result = self.ai_processor.ask_gemini(
            self.prompt.get_structure_content_prompt(
                response_template,
                self.extracted_data.get("raw_image_text", ""),
                self.extracted_data.get("xml_metadata", ""),
                self.extracted_data.get("comparison_analysis", "Not available"),
            )
        )

        self.extracted_data["structured_result"] = self.utility_manager.structure_json(
            structured_result
        )

        # Step 5: Generate HTML
        print("Step 5: Generating HTML...")
        self.extracted_data["html_content"] = self.html_processor.generate_html(
            self.extracted_data.get("structured_result", "")
        )

        # Step 6: Saving results
        self.data_saver.save_processing_data(output_path, self.extracted_data)

        # Return results
        return {
            "all_data": self.extracted_data,
            "html_content": self.extracted_data["html_content"],
            "structured_content": self.extracted_data["structured_result"],
        }
