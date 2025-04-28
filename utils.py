import json
import os
import shutil
from typing import Dict, Any, Optional


class UtilityManager:
    def structure_json(self, result: Optional[str]) -> Dict[str, Any]:
        # Handle None result
        if result is None:
            return {"error": "No response received", "raw_response": None}
            
        # Try to extract JSON from the response
        try:
            # Find JSON pattern in the response
            start_idx = result.find("{")
            end_idx = result.rfind("}") + 1

            if start_idx >= 0 and end_idx > start_idx:
                json_str = result[start_idx:end_idx]
                structured_content = json.loads(json_str)
                return structured_content
            else:
                return {
                    "error": "Could not extract JSON from response",
                    "raw_response": result,
                }
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in response", "raw_response": result}

    def delete_folder_if_exists(self, folder_path: str):
        if os.path.exists(folder_path):
            try:
                shutil.rmtree(folder_path)
                print(f"Folder '{os.path.relpath(folder_path) }' deleted successfully.")
            except Exception as e:
                print(f"Error deleting folder '{folder_path}': {e}")
        else:
            print(f"Folder '{folder_path}' does not exist.")