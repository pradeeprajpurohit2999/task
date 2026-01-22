import xml.etree.ElementTree as ET
import re

def parse_xml():
    try:
        with open('document.xml', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple regex to extract text from w:t tags
        texts = re.findall(r'<w:t(?: [^>]*)?>(.*?)</w:t>', content)
        print('\n'.join(texts))
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    parse_xml()
