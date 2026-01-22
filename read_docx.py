import zipfile
import xml.etree.ElementTree as ET
import sys

def read_docx(file_path):
    try:
        with zipfile.ZipFile(file_path) as docx:
            xml_content = docx.read('word/document.xml')
            tree = ET.fromstring(xml_content)
            
            with open('document.xml', 'wb') as f:
                f.write(xml_content)
            return "Extracted document.xml"
    except Exception as e:
        return f"Error reading docx: {str(e)}"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(read_docx(sys.argv[1]))
    else:
        print("Usage: python read_docx.py <path_to_docx>")
