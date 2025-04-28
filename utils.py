import json
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
                structured_result = json.loads(json_str)
                return structured_result
            else:
                return {
                    "error": "Could not extract JSON from response",
                    "raw_response": result,
                }
        except json.JSONDecodeError:
            return {"error": "Invalid JSON in response", "raw_response": result}
