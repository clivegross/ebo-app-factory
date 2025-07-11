import xml.etree.ElementTree as ET
from .ebo_xml_builder import EBOXMLBuilder
from .html_compression_utils import compress_and_encode_html
from .generate_schneider_uid import (
    generate_html_file_uid,
)


class EBOHTMLFileBuilder(EBOXMLBuilder):
    """
    A class to build HTML File objects and their corresponding ObjectTypes as XML structures for importing into EBO.
    This class extends the EBOXMLBuilder class and provides methods to create
    HTML File-related XML elements with compressed file contents.

    Example XML structure for the object:
    <OI NAME="CIT-WOD-CCTV-B01-B-001" TYPE="udt.apsutrxlanbe5eerqx5ddeybmm.ubsvymz6thv3uo6sr3ieghdenw2d52hd"
        DESCR="{{Description}}" NOTE1="{{Note1}}" NOTE2="{{Note2}}"/>

    Example XML structure for the object type:
    <ObjectType Name="udt.apsutrxlanbe5eerqx5ddeybmm.ubsvymz6thv3uo6sr3ieghdenw2d52hd"
                DisplayName=""
                Description=""
                Base="client.HTML"
                Icon=""
                Abstract="0"
                Implements=""
                DefaultProperty=""
                Version="1">
      <PropertyTab Name="BASIC">
        <PropertyGroup Name="Config">
          <Parameter Name="File" ...>
            <InitValue Null="0">
              <FileContents Size="4240"><![CDATA[...compressed HTML...]]></FileContents>
            </InitValue>
          </Parameter>
        </PropertyGroup>
      </PropertyTab>
    </ObjectType>

    Example usage:
        builder = EBOHTMLFileBuilder()

        # Create HTML file object and its object type
        html_content = "<html><body><h1>Test</h1></body></html>"
        html_obj, object_type = builder.create_html_file_with_type(
            name="CIT-WOD-CCTV-B01-B-001",
            html_content=html_content,
            description="{{Description}}",
            note1="{{Note1}}",
            note2="{{Note2}}"
        )

        # Add both to the builder
        builder.add_object_type(object_type)
        builder.add_to_exported_objects(html_obj)

        # Or use convenience method
        builder.create_and_add_html_file(
            name="CIT-WOD-CCTV-B01-B-002",
            html_content=html_content
        )

        # Or load HTML from file and add directly
        builder.create_and_add_html_file_from_file(
            name="CIT-WOD-CCTV-B01-B-003",
            html_file_path="path/to/file.html",
            description="{{Description}}",
            note1="{{Note1}}",
            note2="{{Note2}}"
        )
    """

    def __init__(self, ebo_version="6.0.4.90", server_full_path="/Server 1"):
        super().__init__(ebo_version, server_full_path)

    def create_html_file_object(
        self, name, object_type_uid, description=None, note1=None, note2=None
    ):
        """
        Create an HTML File object XML element.

        :param name: The name of the HTML file object.
        :param object_type_uid: The unique identifier for the object type.
        :param description: Optional description for the object.
        :param note1: Optional Note1 for the object.
        :param note2: Optional Note2 for the object.
        :return: An XML element representing the HTML file object.
        """
        attribs = {
            "NAME": name,
            "TYPE": object_type_uid,
        }

        if description is not None:
            attribs["DESCR"] = description
        if note1 is not None:
            attribs["NOTE1"] = note1
        if note2 is not None:
            attribs["NOTE2"] = note2

        html_obj = ET.Element("OI", attribs)
        return html_obj

    def create_html_object_type(
        self, object_type_uid, html_content, display_name="", description=""
    ):
        """
        Create an HTML File ObjectType XML element with compressed file contents.

        :param object_type_uid: The unique identifier for this object type.
        :param html_content: The HTML content as a string.
        :param display_name: Optional display name for the object type.
        :param description: Optional description for the object type.
        :return: An XML element representing the HTML file object type.
        """
        # Create the ObjectType element
        object_type = ET.Element("ObjectType")
        object_type.set("Name", object_type_uid)
        object_type.set("DisplayName", display_name)
        object_type.set("Description", description)
        object_type.set("Base", "client.HTML")
        object_type.set("Icon", "")
        object_type.set("Abstract", "0")
        object_type.set("Implements", "")
        object_type.set("DefaultProperty", "")
        object_type.set("Version", "1")

        # Create PropertyTab
        prop_tab = ET.SubElement(object_type, "PropertyTab")
        prop_tab.set("Name", "BASIC")

        # Create PropertyGroup
        prop_group = ET.SubElement(prop_tab, "PropertyGroup")
        prop_group.set("Name", "Config")

        # Create Parameter for File
        parameter = ET.SubElement(prop_group, "Parameter")
        parameter.set("Name", "File")
        parameter.set("DisplayName", "File")
        parameter.set("Description", "")
        parameter.set("Visibility", "Normal")
        parameter.set("Optional", "0")
        parameter.set("ReadOnly", "0")
        parameter.set("Static", "1")
        parameter.set("RTWriteable", "0")
        parameter.set("Unique", "No")
        parameter.set("Copy", "0")
        parameter.set("Nullable", "0")

        # Create Type element
        type_elem = ET.SubElement(parameter, "Type")
        type_elem.set("Configurable", "No")
        type_elem.set("Value", "system.pt.file.HTMLFile")

        # Create Unit element
        unit_elem = ET.SubElement(parameter, "Unit")
        unit_elem.set("Configurable", "No")
        unit_elem.set("Value", "0x10001")

        # Create InitValue
        init_value = ET.SubElement(parameter, "InitValue")
        init_value.set("Null", "0")

        # Create FileContents with compressed HTML
        try:
            compressed_html = compress_and_encode_html(html_content)
            if compressed_html:
                filecontents = ET.SubElement(init_value, "FileContents")
                filecontents.set("Size", str(len(compressed_html)))
                # Store the compressed HTML - we'll handle CDATA during XML output
                filecontents.text = compressed_html
            else:
                raise ValueError("Failed to compress and encode HTML content")
        except Exception as e:
            raise ValueError(f"Error processing HTML content: {e}")

        return object_type

    def create_html_file_with_type(
        self,
        name,
        html_content,
        description=None,
        note1=None,
        note2=None,
        object_type_uid=None,
        namespace_seed=None,
        object_seed=None,
    ):
        """
        Create both an HTML file object and its corresponding object type.

        :param name: The name of the HTML file object.
        :param html_content: The HTML content as a string.
        :param description: Optional description for the object.
        :param note1: Optional Note1 for the object.
        :param note2: Optional Note2 for the object.
        :param object_type_uid: Optional custom UID for the object type. If None, generates one.
        :param namespace_seed: Optional seed for reproducible namespace generation.
        :param object_seed: Optional seed for reproducible object ID generation.
        :return: Tuple of (html_object, object_type) XML elements.
        """
        # Generate UID if not provided - use HTML-specific UID for EBO compatibility
        if object_type_uid is None:
            object_type_uid = generate_html_file_uid(
                html_content, prefix="udt", ebo_version=self._ebo_version
            )

        # Create the object type first
        object_type = self.create_html_object_type(
            object_type_uid=object_type_uid,
            html_content=html_content,
            display_name="",
            description="",
        )

        # Create the HTML file object
        html_obj = self.create_html_file_object(
            name=name,
            object_type_uid=object_type_uid,
            description=description,
            note1=note1,
            note2=note2,
        )

        return html_obj, object_type

    def create_and_add_html_file(
        self,
        name,
        html_content,
        description=None,
        note1=None,
        note2=None,
        object_type_uid=None,
        namespace_seed=None,
        object_seed=None,
    ):
        """
        Convenience method to create an HTML file object and object type, then add them to the builder.

        :param name: The name of the HTML file object.
        :param html_content: The HTML content as a string.
        :param description: Optional description for the object.
        :param note1: Optional Note1 for the object.
        :param note2: Optional Note2 for the object.
        :param object_type_uid: Optional custom UID for the object type. If None, generates one.
        :param namespace_seed: Optional seed for reproducible namespace generation.
        :param object_seed: Optional seed for reproducible object ID generation.
        :return: Tuple of (html_object, object_type) XML elements that were added.
        """
        html_obj, object_type = self.create_html_file_with_type(
            name=name,
            html_content=html_content,
            description=description,
            note1=note1,
            note2=note2,
            object_type_uid=object_type_uid,
            namespace_seed=namespace_seed,
            object_seed=object_seed,
        )

        # Add to the builder
        self.add_object_type(object_type)
        self.add_to_exported_objects(html_obj)

        return html_obj, object_type

    def create_html_file_from_file(
        self,
        name,
        html_file_path,
        description=None,
        note1=None,
        note2=None,
        object_type_uid=None,
        namespace_seed=None,
        object_seed=None,
    ):
        """
        Create an HTML file object and object type from an HTML file on disk.

        :param name: The name of the HTML file object.
        :param html_file_path: Path to the HTML file to read.
        :param description: Optional description for the object.
        :param note1: Optional Note1 for the object.
        :param note2: Optional Note2 for the object.
        :param object_type_uid: Optional custom UID for the object type. If None, generates one.
        :param namespace_seed: Optional seed for reproducible namespace generation.
        :param object_seed: Optional seed for reproducible object ID generation.
        :return: Tuple of (html_object, object_type) XML elements.
        """
        try:
            with open(html_file_path, "r", encoding="utf-8") as f:
                html_content = f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"HTML file not found: {html_file_path}")
        except Exception as e:
            raise Exception(f"Error reading HTML file {html_file_path}: {e}")

        return self.create_html_file_with_type(
            name=name,
            html_content=html_content,
            description=description,
            note1=note1,
            note2=note2,
            object_type_uid=object_type_uid,
            namespace_seed=namespace_seed,
            object_seed=object_seed,
        )

    def create_and_add_html_file_from_file(
        self,
        name,
        html_file_path,
        description=None,
        note1=None,
        note2=None,
        object_type_uid=None,
        namespace_seed=None,
        object_seed=None,
    ):
        """
        Convenience method to create an HTML file object and object type from an HTML file on disk,
        then add them to the builder.

        :param name: The name of the HTML file object.
        :param html_file_path: Path to the HTML file to read.
        :param description: Optional description for the object.
        :param note1: Optional Note1 for the object.
        :param note2: Optional Note2 for the object.
        :param object_type_uid: Optional custom UID for the object type. If None, generates one.
        :param namespace_seed: Optional seed for reproducible namespace generation.
        :param object_seed: Optional seed for reproducible object ID generation.
        :return: Tuple of (html_object, object_type) XML elements that were added.
        """
        html_obj, object_type = self.create_html_file_from_file(
            name=name,
            html_file_path=html_file_path,
            description=description,
            note1=note1,
            note2=note2,
            object_type_uid=object_type_uid,
            namespace_seed=namespace_seed,
            object_seed=object_seed,
        )

        # Add to the builder
        self.add_object_type(object_type)
        self.add_to_exported_objects(html_obj)

        return html_obj, object_type

    def to_pretty_xml(self):
        """
        Converts the XML object to a pretty-printed string with proper CDATA sections for FileContents.
        Returns:
            str: Pretty-printed XML string with CDATA-wrapped FileContents.
        """
        # Get the base XML string
        xml_str = super().to_pretty_xml()

        # Replace FileContents text with CDATA sections
        # Pattern: <FileContents Size="xxx">base64content</FileContents>
        # Replace with: <FileContents Size="xxx"><![CDATA[base64content]]></FileContents>
        import re

        def replace_filecontents(match):
            size_attr = match.group(1)
            content = match.group(2)
            return (
                f'<FileContents Size="{size_attr}"><![CDATA[{content}]]></FileContents>'
            )

        # Use regex to find and replace FileContents elements
        pattern = r'<FileContents Size="(\d+)">([^<]*)</FileContents>'
        xml_str = re.sub(pattern, replace_filecontents, xml_str)

        return xml_str


if __name__ == "__main__":
    # Example usage
    builder = EBOHTMLFileBuilder(ebo_version="6.0.4.90")

    # Example HTML content
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CCTV Camera View</title>
</head>
<body>
    <h1>CIT-WOD-CCTV-B01-B-001</h1>
    <p>CCTV Camera monitoring for Building 1</p>
    <div>
        <iframe src="http://camera.example.com/view1" width="640" height="480"></iframe>
    </div>
</body>
</html>"""

    # Create and add HTML file with placeholders
    html_obj, object_type = builder.create_and_add_html_file(
        name="CIT-WOD-CCTV-B01-B-001",
        html_content=html_content,
        description="{{Description}}",
        note1="{{Note1}}",
        note2="{{Note2}}",
    )

    print("HTML Object UID:", object_type.get("Name"))
    print("\nGenerated XML:")
    print(builder.to_pretty_xml())

    # Write to file
    builder.write_xml("html_file_example.xml")
    print("\nXML written to html_file_example.xml")
