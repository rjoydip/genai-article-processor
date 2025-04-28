from typing import Optional, Dict, Any
from modules.ai_processor import AIProcessor
from modules.prompt_manager import PromptManager


class HTMLProcessor:
    def __init__(self):
        self.prompt = PromptManager()
        self.ai_processor = AIProcessor()

    def generate_html(self, result: Optional[str] = None) -> Optional[str]:
        """Generate HTML representation of the article."""
        if not result:
            return "Error: Missing structured result. Run structure_content step first."
        else:
            # Try to extract HTML from response
            html_start = result.find("<html")
            html_end = result.rfind("</html>") + 7

            if html_start >= 0 and html_end > html_start:
                html_code = result[html_start:html_end]
                return html_code
            else:
                return result  # Return the full response if we couldn't extract HTML
