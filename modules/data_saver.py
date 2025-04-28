import asyncio
from functools import partial
import json
import os

from config import PROCESSED_FILE_NAME


class DataSaver:
    async def _save_json(self, filepath, data):
        """Save JSON data asynchronously."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self._write_json(filepath, data))

    def _write_json(self, filepath, data):
        """Helper method to write JSON - runs in executor."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)

    async def _save_text(self, filepath, text):
        """Save text data asynchronously."""
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: self._write_text(filepath, text))

    def _write_text(self, filepath, text):
        """Helper method to write text - runs in executor."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(text)

    async def save_processed_data(self, output_dir, extracted_data):
        """Save all processing results to files."""
        # Create directory
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None, partial(os.makedirs, output_dir, exist_ok=True)
        )

        save_tasks = []

        # Save RAW text
        if extracted_data["raw_image_text"]:
            structured_content_path = os.path.join(
                output_dir, f"{PROCESSED_FILE_NAME}_raw.txt"
            )
            save_tasks.append(
                self._save_text(
                    structured_content_path, extracted_data["raw_image_text"]
                )
            )

        # Save structured result as JSON
        if extracted_data["structured_content"]:
            structured_content_path = os.path.join(
                output_dir, f"{PROCESSED_FILE_NAME}_structured_content.json"
            )
            save_tasks.append(
                self._save_json(
                    structured_content_path, extracted_data["structured_content"]
                )
            )

        # Save XML content
        if extracted_data["xml_metadata"]:
            xml_metadata_path = os.path.join(
                output_dir, f"{PROCESSED_FILE_NAME}_xml_metadata.json"
            )
            save_tasks.append(
                self._save_json(xml_metadata_path, extracted_data["xml_metadata"])
            )

        # Save HTML content
        if extracted_data["html_content"]:
            html_path = os.path.join(output_dir, f"{PROCESSED_FILE_NAME}.html")
            save_tasks.append(
                self._save_text(html_path, extracted_data["html_content"])
            )

        # Save combined content
        if extracted_data["combined_content"]:
            combined_content__path = os.path.join(
                output_dir, f"{PROCESSED_FILE_NAME}_combined_content.json"
            )
            save_tasks.append(
                self._save_json(
                    combined_content__path, extracted_data["combined_content"]
                )
            )

        # Save full processing data
        full_data_path = os.path.join(output_dir, f"{PROCESSED_FILE_NAME}_full.json")
        # Filter out any non-serializable data
        serializable_data = {}
        for key, value in extracted_data.items():
            if isinstance(value, (dict, list, str, int, float, bool, type(None))):
                serializable_data[key] = value

        save_tasks.append(self._save_json(full_data_path, serializable_data))

        # Wait for all save operations to complete
        await asyncio.gather(*save_tasks)

        return f"Results saved to {output_dir}"
