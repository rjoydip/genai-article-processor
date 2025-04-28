import json
import os

from config import PROCESSED_FILE_NAME

class DataSaver:
    def save_processed_data(self, output_dir, extracted_data):
        """Save all processing results to files."""
        os.makedirs(output_dir, exist_ok=True)

        # Save RAW text
        if extracted_data["raw_image_text"]:
            with open(
                os.path.join(output_dir, f"{PROCESSED_FILE_NAME}_raw.txt"), "w", encoding="utf-8"
            ) as f:
                f.write(extracted_data["raw_image_text"])

        # Save structured result as JSON
        if extracted_data["structured_content"]:
            with open(
                os.path.join(output_dir, f"{PROCESSED_FILE_NAME}_structured_content.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(extracted_data["structured_content"], f, indent=2)

        # Save XML content
        if extracted_data["xml_metadata"]:
            with open(
                os.path.join(output_dir, f"{PROCESSED_FILE_NAME}_xml_metadata.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(extracted_data["xml_metadata"], f, indent=2)


        # Save HTML content
        if extracted_data["html_content"]:
            with open(
                os.path.join(output_dir, f"{PROCESSED_FILE_NAME}.html"), "w", encoding="utf-8"
            ) as f:
                f.write(extracted_data["html_content"])

        # Save combined content
        if extracted_data["combined_content"]:
            with open(
                os.path.join(output_dir, f"{PROCESSED_FILE_NAME}_combined_content.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(extracted_data["combined_content"], f, indent=2)

        # Save full processing data
        with open(
            os.path.join(output_dir, f"{PROCESSED_FILE_NAME}_full.json"), "w", encoding="utf-8"
        ) as f:
            # Filter out any non-serializable data
            serializable_data = {}
            for key, value in extracted_data.items():
                if isinstance(value, (dict, list, str, int, float, bool, type(None))):
                    serializable_data[key] = value

            json.dump(serializable_data, f, indent=2)

        return f"Results saved to {output_dir}"
