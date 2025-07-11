#!/usr/bin/env python3
"""
Unit tests for EBOHTMLFileBuilder class.
"""

import os
import sys
import unittest
import xml.etree.ElementTree as ET
import tempfile

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ebo_app_factory.html_file_builder import EBOHTMLFileBuilder
from ebo_app_factory.html_compression_utils import decode_and_decompress_cdata


class TestEBOHTMLFileBuilder(unittest.TestCase):
    """Test cases for EBOHTMLFileBuilder class."""

    def setUp(self):
        """Set up test fixtures."""
        self.builder = EBOHTMLFileBuilder(
            ebo_version="6.0.4.90", server_full_path="/Test Server"
        )
        self.test_html = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Test HTML File</title>
</head>
<body>
    <h1>{{Description}}</h1>
    <p>Test content with placeholders:</p>
    <ul>
        <li>Note 1: {{Note1}}</li>
        <li>Note 2: {{Note2}}</li>
    </ul>
    <script>console.log('Test script');</script>
</body>
</html>"""

    def test_create_html_file_object(self):
        """Test creating an HTML file object."""
        object_type_uid = "test.uid.example"
        html_obj = self.builder.create_html_file_object(
            name="Test-HTML-Object",
            object_type_uid=object_type_uid,
            description="{{Description}}",
            note1="{{Note1}}",
            note2="{{Note2}}",
        )

        self.assertEqual(html_obj.tag, "OI")
        self.assertEqual(html_obj.get("NAME"), "Test-HTML-Object")
        self.assertEqual(html_obj.get("TYPE"), object_type_uid)
        self.assertEqual(html_obj.get("DESCR"), "{{Description}}")
        self.assertEqual(html_obj.get("NOTE1"), "{{Note1}}")
        self.assertEqual(html_obj.get("NOTE2"), "{{Note2}}")

    def test_create_html_object_type(self):
        """Test creating an HTML object type."""
        object_type_uid = "test.uid.example"
        object_type = self.builder.create_html_object_type(
            object_type_uid=object_type_uid, html_content=self.test_html
        )

        self.assertEqual(object_type.tag, "ObjectType")
        self.assertEqual(object_type.get("Name"), object_type_uid)
        self.assertEqual(object_type.get("Base"), "client.HTML")
        self.assertEqual(object_type.get("Version"), "1")

        # Check for FileContents
        filecontents = object_type.find(".//FileContents")
        self.assertIsNotNone(filecontents)
        self.assertIsNotNone(filecontents.get("Size"))
        self.assertIsNotNone(filecontents.text)

    def test_create_html_file_with_type(self):
        """Test creating both HTML file object and object type together."""
        html_obj, object_type = self.builder.create_html_file_with_type(
            name="Test-Combined",
            html_content=self.test_html,
            description="Test description",
        )

        # Check that both elements are created
        self.assertEqual(html_obj.tag, "OI")
        self.assertEqual(object_type.tag, "ObjectType")

        # Check that they reference each other correctly
        object_type_uid = object_type.get("Name")
        self.assertEqual(html_obj.get("TYPE"), object_type_uid)
        self.assertIsNotNone(object_type_uid)
        self.assertTrue(object_type_uid.startswith("udt."))

    def test_create_and_add_html_file(self):
        """Test the convenience method that creates and adds to builder."""
        html_obj, object_type = self.builder.create_and_add_html_file(
            name="Test-Added", html_content=self.test_html
        )

        # Check that elements were added to the builder
        xml_content = self.builder.to_pretty_xml()
        self.assertIn("Test-Added", xml_content)
        self.assertIn(object_type.get("Name"), xml_content)

    def test_xml_structure_validation(self):
        """Test that generated XML has correct structure."""
        self.builder.create_and_add_html_file(
            name="Structure-Test", html_content=self.test_html
        )

        # Generate XML and parse it
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            self.builder.write_xml(f.name)
            xml_file = f.name

        try:
            tree = ET.parse(xml_file)
            root = tree.getroot()

            # Validate root structure
            self.assertEqual(root.tag, "ObjectSet")
            self.assertEqual(root.get("Version"), "6.0.4.90")

            # Validate sections exist
            self.assertIsNotNone(root.find("MetaInformation"))
            self.assertIsNotNone(root.find("Types"))
            self.assertIsNotNone(root.find("ExportedObjects"))

            # Validate object type structure
            object_type = root.find(".//ObjectType")
            self.assertIsNotNone(object_type)
            self.assertEqual(object_type.get("Base"), "client.HTML")

            # Validate PropertyTab structure
            prop_tab = object_type.find("PropertyTab")
            self.assertIsNotNone(prop_tab)
            self.assertEqual(prop_tab.get("Name"), "BASIC")

            # Validate FileContents
            filecontents = object_type.find(".//FileContents")
            self.assertIsNotNone(filecontents)
            self.assertIsNotNone(filecontents.get("Size"))
            self.assertIsNotNone(filecontents.text)

        finally:
            os.unlink(xml_file)

    def test_html_round_trip(self):
        """Test that HTML can be compressed, encoded, then decoded back correctly."""
        self.builder.create_and_add_html_file(
            name="Round-Trip-Test", html_content=self.test_html
        )

        # Generate XML
        with tempfile.NamedTemporaryFile(mode="w", suffix=".xml", delete=False) as f:
            self.builder.write_xml(f.name)
            xml_file = f.name

        try:
            # Extract FileContents CDATA
            tree = ET.parse(xml_file)
            filecontents = tree.find(".//FileContents")
            cdata_content = filecontents.text

            # Decode and decompress
            decoded_html = decode_and_decompress_cdata(cdata_content)

            # Normalize whitespace for comparison
            original_normalized = " ".join(self.test_html.split())
            decoded_normalized = " ".join(decoded_html.split())

            self.assertEqual(original_normalized, decoded_normalized)

            # Check for specific content
            self.assertIn("{{Description}}", decoded_html)
            self.assertIn("{{Note1}}", decoded_html)
            self.assertIn("{{Note2}}", decoded_html)
            self.assertIn("Test script", decoded_html)

        finally:
            os.unlink(xml_file)

    def test_placeholder_support(self):
        """Test that placeholders are preserved in the HTML."""
        html_obj, object_type = self.builder.create_html_file_with_type(
            name="Placeholder-Test",
            html_content=self.test_html,
            description="{{Description}}",
            note1="{{Note1}}",
            note2="{{Note2}}",
        )

        # Check object attributes have placeholders
        self.assertEqual(html_obj.get("DESCR"), "{{Description}}")
        self.assertEqual(html_obj.get("NOTE1"), "{{Note1}}")
        self.assertEqual(html_obj.get("NOTE2"), "{{Note2}}")

        # Check HTML content has placeholders
        filecontents = object_type.find(".//FileContents")
        cdata_content = filecontents.text
        decoded_html = decode_and_decompress_cdata(cdata_content)

        self.assertIn("{{Description}}", decoded_html)
        self.assertIn("{{Note1}}", decoded_html)
        self.assertIn("{{Note2}}", decoded_html)

    def test_custom_uid_generation(self):
        """Test UID generation - now content-based for EBO compatibility."""
        html_obj1, object_type1 = self.builder.create_html_file_with_type(
            name="Custom-UID-Test",
            html_content=self.test_html,
            namespace_seed="test_namespace",
            object_seed="test_object",
        )

        html_obj2, object_type2 = self.builder.create_html_file_with_type(
            name="Custom-UID-Test-2",
            html_content=self.test_html,
            namespace_seed="test_namespace",
            object_seed="test_object",
        )

        # Same content should generate same UID (content-based)
        self.assertEqual(object_type1.get("Name"), object_type2.get("Name"))

        # Different content should generate different UID
        different_html = "<html><body><h1>Different Content</h1></body></html>"
        html_obj3, object_type3 = self.builder.create_html_file_with_type(
            name="Custom-UID-Test-3",
            html_content=different_html,
            namespace_seed="different_namespace",
            object_seed="different_object",
        )

        self.assertNotEqual(object_type1.get("Name"), object_type3.get("Name"))

        # All UIDs should use the correct namespace for HTML files
        uid1 = object_type1.get("Name")
        uid2 = object_type2.get("Name")
        uid3 = object_type3.get("Name")

        self.assertTrue(uid1.startswith("udt.apsutrxlanbe5eerqx5ddeybmm."))
        self.assertTrue(uid2.startswith("udt.apsutrxlanbe5eerqx5ddeybmm."))
        self.assertTrue(uid3.startswith("udt.apsutrxlanbe5eerqx5ddeybmm."))

    def test_error_handling(self):
        """Test error handling for invalid inputs."""
        # Test with invalid HTML (should still work, just compress the invalid content)
        invalid_html = "<html><body><h1>Unclosed tag</body></html>"
        html_obj, object_type = self.builder.create_html_file_with_type(
            name="Invalid-HTML-Test", html_content=invalid_html
        )

        # Should still create objects
        self.assertIsNotNone(html_obj)
        self.assertIsNotNone(object_type)

        # Test with empty HTML
        empty_html = ""
        html_obj, object_type = self.builder.create_html_file_with_type(
            name="Empty-HTML-Test", html_content=empty_html
        )

        self.assertIsNotNone(html_obj)
        self.assertIsNotNone(object_type)

    def test_create_and_add_html_file_from_file(self):
        """Test the convenience method that creates and adds HTML file from disk."""
        # Get path to the test HTML file
        test_data_dir = os.path.join(os.path.dirname(__file__), "data")
        html_file_path = os.path.join(test_data_dir, "basic_test.html")
        
        # Verify the test file exists
        self.assertTrue(os.path.exists(html_file_path), f"Test file not found: {html_file_path}")
        
        # Test the new method
        html_obj, object_type = self.builder.create_and_add_html_file_from_file(
            name="Test-File-HTML",
            html_file_path=html_file_path,
            description="{{Description}}",
            note1="{{Note1}}",
            note2="{{Note2}}"
        )
        
        # Check that both elements are created
        self.assertEqual(html_obj.tag, "OI")
        self.assertEqual(object_type.tag, "ObjectType")
        self.assertEqual(html_obj.get("NAME"), "Test-File-HTML")
        self.assertEqual(html_obj.get("DESCR"), "{{Description}}")
        self.assertEqual(html_obj.get("NOTE1"), "{{Note1}}")
        self.assertEqual(html_obj.get("NOTE2"), "{{Note2}}")
        
        # Check that they reference each other correctly
        object_type_uid = object_type.get("Name")
        self.assertEqual(html_obj.get("TYPE"), object_type_uid)
        self.assertIsNotNone(object_type_uid)
        self.assertTrue(object_type_uid.startswith("udt."))
        
        # Check that elements were added to the builder
        xml_content = self.builder.to_pretty_xml()
        self.assertIn("Test-File-HTML", xml_content)
        self.assertIn(object_type_uid, xml_content)
        
        # Verify HTML content was loaded correctly by checking for placeholders
        filecontents = object_type.find(".//FileContents")
        self.assertIsNotNone(filecontents)
        cdata_content = filecontents.text
        decoded_html = decode_and_decompress_cdata(cdata_content)
        
        # Check for specific placeholders from basic_test.html
        self.assertIn("{{PageTitle}}", decoded_html)
        self.assertIn("{{DeviceName}}", decoded_html)
        self.assertIn("{{Location}}", decoded_html)
        self.assertIn("{{Description}}", decoded_html)
        self.assertIn("{{Temperature}}", decoded_html)
        self.assertIn("{{Humidity}}", decoded_html)
        self.assertIn("{{Note1}}", decoded_html)
        self.assertIn("{{Note2}}", decoded_html)
        
        # Test error handling for non-existent file
        with self.assertRaises(FileNotFoundError):
            self.builder.create_and_add_html_file_from_file(
                name="Non-Existent",
                html_file_path="/path/that/does/not/exist.html"
            )


if __name__ == "__main__":
    unittest.main(verbosity=2)
