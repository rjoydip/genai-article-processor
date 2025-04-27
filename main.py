import os
import json
import argparse
from modules.image_processor import ImageProcessor
from modules.data_saver import DataSaver
from modules.xml_parser import XMLParser
from modules.ai_processor import AIProcessor
from modules.html_generator import HTMLGenerator
from modules.agent import ArticleProcessingAgent
from config import INPUT_FOLDER, PROCESSED_FOLDER, RESPONSE_STRUCTURE


class ArticleProcessor:
    def __init__(self, use_agent="False"):
        self.use_agent = use_agent

        if use_agent == "True":
            self.agent = ArticleProcessingAgent()
        else:
            self.image_processor = ImageProcessor()
            self.xml_parser = XMLParser()
            self.ai_processor = AIProcessor()
            self.html_generator = HTMLGenerator()
            self.data_saver = DataSaver()

    def process_article(self, image_path, xml_path):
        """Process an article image and corresponding XML metadata."""
        if self.use_agent == "True":
            # Use agentic approach
            result = self.agent.process_article(
                image_path, xml_path, RESPONSE_STRUCTURE
            )

            # Save results
            self.agent.save_results(PROCESSED_FOLDER)

            return result
        else:
            # Use modular approach
            extracted_data = {}

            # Step 1: Extract text from image
            extracted_text = self.image_processor.extract_text_from_image(image_path)
            if not extracted_text:
                return {"error": "Failed to extract text from image"}

            extracted_data["raw_image_text"] = extracted_text

            # Find JSON pattern in the response
            extracted_data["structured_result"] = json.dumps(
                "{" + "raw_image_text:" + extracted_data["raw_image_text"] + "}",
                indent=2,
            )

            # Step 2: Parse XML metadata
            xml_metadata = self.xml_parser.parse_metadata(xml_path)
            xml_content_sections = self.xml_parser.extract_content_sections(xml_path)

            extracted_data["xml_metadata"] = xml_metadata
            # Step 3: Process with AI
            comparison_analysis = self.ai_processor.compare_and_process(
                extracted_text, xml_metadata, xml_content_sections
            )

            extracted_data["comparison_analysis"] = comparison_analysis

            # Step 4: Generate HTML
            html_content = self.html_generator.generate_html(comparison_analysis)

            extracted_data["html_content"] = html_content

            # Save results
            self.data_saver.save_processing_data(
                PROCESSED_FOLDER,
                extracted_data,
            )

            # Return combined results
            return extracted_data


def main():
    parser = argparse.ArgumentParser(
        prog="Article Processor",
    )

    parser.add_argument("-n", "--name", type=str, default="article")
    parser.add_argument("-a", "--agent", type=str, default="True")

    args = parser.parse_args()

    # Choose whether to use the agent or not
    processor = ArticleProcessor(use_agent=args.agent)

    # Example usage
    processor.process_article(
        os.path.join(INPUT_FOLDER, f"{args.name}.png"),
        os.path.join(INPUT_FOLDER, f"{args.name}.xml"),
    )

    print("Processing complete. Output saved to the artifacts folder.")


if __name__ == "__main__":
    main()
