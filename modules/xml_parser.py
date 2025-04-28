# modules/xml_parser.py
import asyncio
import xml.etree.ElementTree as ET
from typing import Dict, Any


class XMLParser:
    def _parse_element(self, element: ET.Element) -> Dict[str, Any]:
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

    def _parse_xml_metadata(self, xml_path: str) -> Dict[str, Any]:
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

            return metadata
        except Exception as e:
            print(f"Error parsing XML: {e}")
            return {}

    async def parse_xml_metadata(self, xml_path: str) -> Dict[str, Any]:
        """Parse the XML metadata file asynchronously."""
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, self._parse_xml_metadata, xml_path)
