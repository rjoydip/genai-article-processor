# modules/xml_parser.py
import xml.etree.ElementTree as ET

class XMLParser:
    def parse_metadata(self, xml_file):
        """Extract metadata from the XML file."""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            metadata = {}
            
            # Extract common metadata fields
            for child in root:
                metadata[child.tag] = child.text
                
            return metadata
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return {}
    
    def extract_content_sections(self, xml_file):
        """Extract content sections that might need verification."""
        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            
            content_sections = []
            
            # Look for content sections (adjust based on your XML structure)
            for section in root.findall(".//content") + root.findall(".//paragraph"):
                if section.text:
                    content_sections.append(section.text.strip())
                    
            return content_sections
        except Exception as e:
            print(f"Error extracting content sections: {e}")
            return []