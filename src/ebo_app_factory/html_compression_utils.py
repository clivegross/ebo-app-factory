#!/usr/bin/env python3
"""
Functions to decode and decompress FileContents CDATA from Schneider Electric Building Operation XML exports.
The CDATA contains Base64-encoded, gzip-compressed data.
"""

import base64
import gzip
import xml.etree.ElementTree as ET
from typing import Optional


def extract_cdata_from_xml(xml_file_path: str) -> Optional[str]:
    """
    Extract the FileContents CDATA from a Schneider Electric XML export file.

    Args:
        xml_file_path (str): Path to the XML file

    Returns:
        Optional[str]: The Base64 CDATA content, or None if not found
    """
    try:
        tree = ET.parse(xml_file_path)
        root = tree.getroot()

        # Find the FileContents element
        filecontents = root.find(".//FileContents")
        if filecontents is not None and filecontents.text:
            return filecontents.text.strip()
        else:
            print("FileContents CDATA not found in XML")
            return None

    except ET.ParseError as e:
        print(f"Error parsing XML: {e}")
        return None
    except FileNotFoundError:
        print(f"File not found: {xml_file_path}")
        return None


def decode_and_decompress_cdata(cdata_content: str) -> Optional[str]:
    """
    Decode Base64 and decompress gzip data from CDATA content.

    Args:
        cdata_content (str): Base64-encoded, gzip-compressed data

    Returns:
        Optional[str]: Decompressed content as string, or None if error
    """
    try:
        # Step 1: Decode from Base64
        print("Decoding Base64...")
        compressed_data = base64.b64decode(cdata_content)
        print(f"Base64 decoded. Compressed size: {len(compressed_data)} bytes")

        # Step 2: Decompress gzip
        print("Decompressing gzip...")
        decompressed_data = gzip.decompress(compressed_data)
        print(f"Gzip decompressed. Decompressed size: {len(decompressed_data)} bytes")

        # Step 3: Convert to string (assuming UTF-8 encoding)
        content = decompressed_data.decode("utf-8")

        # Step 4: Fix extra line breaks (normalize line endings)
        # Remove excessive line breaks and normalize to single line breaks
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        # Remove any double line breaks that might have been introduced
        while "\n\n\n" in content:
            content = content.replace("\n\n\n", "\n\n")

        return content

    except base64.binascii.Error as e:
        print(f"Base64 decode error: {e}")
        return None
    except gzip.BadGzipFile as e:
        print(f"Gzip decompression error: {e}")
        return None
    except UnicodeDecodeError as e:
        print(f"UTF-8 decode error: {e}")
        return None
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None


def extract_and_decode_xml_file(
    xml_file_path: str, output_file_path: Optional[str] = None
) -> Optional[str]:
    """
    Complete function to extract CDATA from XML file and decode/decompress it.

    Args:
        xml_file_path (str): Path to the XML file
        output_file_path (Optional[str]): Path to save the decoded content, or None to not save

    Returns:
        Optional[str]: Decompressed content, or None if error
    """
    print(f"Processing XML file: {xml_file_path}")

    # Step 1: Extract CDATA from XML
    cdata_content = extract_cdata_from_xml(xml_file_path)
    if not cdata_content:
        return None

    print(f"CDATA extracted. Base64 length: {len(cdata_content)} characters")

    # Step 2: Decode and decompress
    decoded_content = decode_and_decompress_cdata(cdata_content)
    if not decoded_content:
        return None

    print("Successfully decoded and decompressed content!")

    # Step 3: Save to file if requested
    if output_file_path:
        try:
            with open(output_file_path, "w", encoding="utf-8") as f:
                f.write(decoded_content)
            print(f"Content saved to: {output_file_path}")
        except Exception as e:
            print(f"Error saving file: {e}")

    return decoded_content


def compress_and_encode_html(html_content: str) -> str:
    """
    Compress HTML content with gzip and encode to Base64 for Schneider Electric XML format.

    Args:
        html_content (str): HTML content as string

    Returns:
        str: Base64-encoded, gzip-compressed data
    """
    try:
        # Step 1: Convert string to bytes (UTF-8)
        html_bytes = html_content.encode("utf-8")
        print(f"HTML content size: {len(html_bytes)} bytes")

        # Step 2: Compress with gzip
        compressed_data = gzip.compress(html_bytes)

        # Calculate compression ratio (handle empty content)
        if len(html_bytes) > 0:
            compression_ratio = len(compressed_data) / len(html_bytes)
            print(
                f"Compressed size: {len(compressed_data)} bytes (compression ratio: {compression_ratio:.2%})"
            )
        else:
            print(f"Compressed size: {len(compressed_data)} bytes (empty content)")

        # Step 3: Encode to Base64
        base64_data = base64.b64encode(compressed_data).decode("ascii")
        print(f"Base64 encoded size: {len(base64_data)} characters")

        return base64_data

    except Exception as e:
        print(f"Error compressing and encoding: {e}")
        return None


def create_filecontents_element(
    html_content: str, size: Optional[int] = None
) -> ET.Element:
    """
    Create a FileContents XML element with compressed and encoded HTML content.

    Args:
        html_content (str): HTML content as string
        size (Optional[int]): Size value for the FileContents element (auto-calculated if None)

    Returns:
        ET.Element: FileContents element ready for XML
    """
    # Compress and encode the HTML
    base64_data = compress_and_encode_html(html_content)

    if base64_data is None:
        return None

    # Calculate size if not provided (length of base64 string)
    if size is None:
        size = len(base64_data)

    # Create the FileContents element
    filecontents = ET.Element("FileContents")
    filecontents.set("Size", str(size))

    # Set the text content with CDATA wrapper
    # ElementTree will automatically handle CDATA when the text contains special characters
    # But we need to force CDATA format, so we'll set it properly
    filecontents.text = base64_data

    return filecontents


def html_file_to_filecontents_element(html_file_path: str) -> ET.Element:
    """
    Read an HTML file and create a FileContents XML element.

    Args:
        html_file_path (str): Path to the HTML file

    Returns:
        ET.Element: FileContents element ready for XML
    """
    try:
        with open(html_file_path, "r", encoding="utf-8") as f:
            html_content = f.read()

        print(f"Read HTML file: {html_file_path}")
        return create_filecontents_element(html_content)

    except FileNotFoundError:
        print(f"HTML file not found: {html_file_path}")
        return None
    except Exception as e:
        print(f"Error reading HTML file: {e}")
        return None


def main():
    """
    Example usage of the functions.
    """
    print("=== Schneider Electric XML Processor ===\n")

    # Example 1: Extract and decode existing XML
    print("1. EXTRACTING from existing XML:")
    xml_file = r"Test EBO Export.xml"
    output_file = r"output.html"

    content = extract_and_decode_xml_file(xml_file, output_file)

    if content:
        print(f"✅ Successfully extracted {len(content)} characters")
        print(f"   Saved to: {output_file}")
    else:
        print("❌ Failed to extract content")

    print("\n" + "=" * 60 + "\n")

    # Example 2: Create new XML from HTML content
    print("2. CREATING new XML from HTML:")

    if content:  # Use the extracted content
        # Create a new XML export
        new_xml_path = r"c:\Users\Administrator\Desktop\CIT Woden\new_export.xml"
        # success = save_html_as_schneider_xml(content, "Test-HTML-Export", new_xml_path)

        # if success:
        #     print(f"✅ Successfully created new XML export")
        # else:
        #     print("❌ Failed to create XML export")

    print("\n" + "=" * 60 + "\n")

    # Example 3: Demonstrate round-trip (extract -> modify -> re-encode)
    print("3. ROUND-TRIP test (extract -> modify -> re-encode):")

    if content:
        # Modify the HTML content slightly
        modified_content = content.replace(
            "<title>CIT-WOD-CCTV-B01-B-001</title>",
            "<title>CIT-WOD-CCTV-B01-B-001 (Modified)</title>",
        )

        # Create FileContents element
        filecontents_elem = create_filecontents_element(modified_content)

        if filecontents_elem is not None:
            print(f"✅ Successfully created FileContents element")
            print(f"   Size attribute: {filecontents_elem.get('Size')}")
            print(f"   CDATA length: {len(filecontents_elem.text)} characters")

            # Show the first 100 characters of the Base64 data
            print(f"   CDATA preview: {filecontents_elem.text[:100]}...")
        else:
            print("❌ Failed to create FileContents element")

    print("\n" + "=" * 60 + "\n")

    # Example 4: Create XML from a simple HTML string
    print("4. CREATE XML from simple HTML:")

    simple_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Simple Test Page</title>
</head>
<body>
    <h1>Hello Schneider Electric!</h1>
    <p>This is a test HTML page created programmatically.</p>
</body>
</html>"""

    simple_xml_path = r"simple_test_export.xml"
    # success = save_html_as_schneider_xml(
    #     simple_html, "Simple-Test-Page", simple_xml_path
    # )

    # if success:
    #     print(f"✅ Successfully created simple XML export")
    #     print(f"   Saved to: {simple_xml_path}")
    # else:
    #     print("❌ Failed to create simple XML export")


if __name__ == "__main__":
    main()
