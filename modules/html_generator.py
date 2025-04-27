import json
from bs4 import BeautifulSoup


class HTMLGenerator:
    def generate_html(self, structured_response):
        """Generate HTML from the structured response."""
        try:
            # Parse the response JSON
            if isinstance(structured_response, str):
                data = json.loads(structured_response)
            else:
                data = structured_response

            # Create HTML structure
            soup = BeautifulSoup("", "html.parser")

            # Create the basic HTML structure
            html = soup.new_tag("html")
            soup.append(html)

            head = soup.new_tag("head")
            html.append(head)

            # Add metadata
            title_tag = soup.new_tag("title")
            title_tag.string = data.get("title", "Article")
            head.append(title_tag)

            # Add some basic styling
            style = soup.new_tag("style")
            style.string = ""
            head.append(style)

            # Create body
            body = soup.new_tag("body")
            html.append(body)

            # Add title
            h1 = soup.new_tag("h1")
            h1.string = data.get("title", "Article")
            body.append(h1)

            # Add author and date
            metadata_div = soup.new_tag("div", attrs={"class": "metadata"})
            metadata_text = f"By {data.get('author', 'Unknown')} | {data.get('date', 'Unknown date')}"
            metadata_div.string = metadata_text
            body.append(metadata_div)

            # Add content paragraphs
            for paragraph in data.get("content", []):
                p = soup.new_tag("p")
                p.string = paragraph
                body.append(p)

            return str(soup)
        except Exception as e:
            print(f"Error generating HTML: {e}")
            return f"<html><body><p>Error generating HTML: {e}</p></body></html>"
