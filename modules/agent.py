import asyncio
from concurrent.futures import ThreadPoolExecutor
from functools import partial
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
        self.extracted_data: Dict[str, Any] = {
            "raw_image_text": None,
            "xml_metadata": None,
            "combined_content": None,
            "structured_content": None,
            "html_content": None,
        }

    async def process_article(
        self,
        image_path: str,
        xml_path: str,
        response_template: Dict[str, Any],
        output_path: str,
    ) -> Dict[str, Any]:
        # Setup a thread pool for CPU-bound tasks
        executor = ThreadPoolExecutor(max_workers=3)
        loop = asyncio.get_event_loop()

        print("Starting article processing...")

        # Step 1 & 2: Extract text from image and Parse XML metadata in parallel
        print("Steps 1 & 2: Extracting text and parsing XML in parallel...")

        raw_image_task = self.ai_processor.ask_ai(
            self.prompt.get_content_extraction_prompt(), image_path
        )

        xml_metadata_task = self.xml_parser.parse_xml_metadata(xml_path)

        # Wait for both tasks to complete
        raw_image_text, xml_metadata = await asyncio.gather(
            raw_image_task, xml_metadata_task
        )

        self.extracted_data["raw_image_text"] = raw_image_text
        self.extracted_data["xml_metadata"] = xml_metadata

        # Step 3: Combined content
        print("Step 3: Combined content...")
        combined_content = await self.ai_processor.ask_ai(
            self.prompt.get_combined_prompt(
                self.extracted_data.get("raw_image_text", ""),
                self.extracted_data.get("xml_metadata", ""),
            )
        )

        # Run JSON structuring in thread pool to avoid blocking
        self.extracted_data[
            "combined_content"
        ] = await self.utility_manager.structure_json_async(combined_content)

        # Step 4: Structure content
        print("Step 4: Structuring content...")
        structured_content = await self.ai_processor.ask_ai(
            self.prompt.get_structure_content_prompt(
                response_template,
                self.extracted_data.get("raw_image_text", ""),
                self.extracted_data.get("xml_metadata", ""),
                self.extracted_data.get("combined_content", "Not available"),
            )
        )

        # Structure JSON in thread pool
        self.extracted_data[
            "structured_content"
        ] = await self.utility_manager.structure_json_async(structured_content)

        # Step 5: Generate HTML
        print("Step 5: Generating HTML...")
        html_content = await self.ai_processor.ask_ai(
            self.prompt.get_html_prompt(
                self.extracted_data.get("structured_content", "")
            )
        )

        self.extracted_data["html_content"] = await loop.run_in_executor(
            executor, partial(self.html_processor.generate_html, html_content)
        )

        # Step 6: Saving results
        await self.data_saver.save_processed_data(output_path, self.extracted_data)

        # Return results
        return self.extracted_data
