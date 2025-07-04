import os
from ebo_app_factory.xml_app_factory import (
    ApplicationFactory,
    ApplicationFactoryManager,
    ApplicationTemplate,
    FactoryInputsFromSpreadsheet,
)


def test_application_factory_manager_creates_xml(tmp_path):
    # Arrange: Set up paths to test data
    test_dir = os.path.dirname(__file__)
    item_workbook = "items.xlsx"
    template1_filename = (
        "Emergency Lighting Group ICG-L04M EBO app Export 2024-04-19.xml"
    )
    template2_filename = "Zoneworks XT Hive Controller 1 EBO app Export 2024-04-19.xml"
    template1_path = os.path.join(test_dir, "data", template1_filename)
    template2_path = os.path.join(test_dir, "data", template2_filename)
    item_workbook_path = os.path.join(test_dir, "data", item_workbook)
    output_path_prefix = os.path.join(tmp_path, "output")

    template_map = {
        "ICG": {"templateFilename": template1_path},
        "IT2_IT3": {"templateFilename": template1_path},
        "IT1": {"templateFilename": template1_path},
        "ISD": {"templateFilename": template1_path},
        "controllers": {"templateFilename": template2_path},
    }

    # Instantiate helpers

    # Act: Create the XML
    app_factory_manager = ApplicationFactoryManager(
        template_map=template_map,
        xlfile=item_workbook_path,
        max_items_per_file=5,
        xml_out_file_prefix=output_path_prefix,
    )
    app_factory_manager.make_documents()

    # Assert: Output file is created and contains expected root element
    output_path = os.path.join(tmp_path, "output_ISD_2.xml")
    assert os.path.exists(output_path), f"Output file {output_path} does not exist"
    with open(output_path, "r", encoding="utf-8") as f:
        xml_content = f.read()
    assert "<ObjectSet" in xml_content
    assert "ISD-L23M" in xml_content, "Expected item not found in XML content"


def test_application_factory_creates_xml(tmp_path):
    # Arrange: Set up paths to test data
    test_dir = os.path.dirname(__file__)
    item_workbook = "items.xlsx"
    template_filename = (
        "Emergency Lighting Group ICG-L04M EBO app Export 2024-04-19.xml"
    )
    template_path = os.path.join(test_dir, "data", template_filename)
    item_workbook_path = os.path.join(test_dir, "data", item_workbook)
    output_xml_path = os.path.join(tmp_path, "output.xml")

    # Instantiate helpers
    app_template = ApplicationTemplate(template_path)
    factory_inputs = FactoryInputsFromSpreadsheet(xlfile=item_workbook_path)

    # Act: Create the XML
    app_factory = ApplicationFactory(
        template_child_elements_dict=app_template.template_child_elements_dict,
        factory_placeholders=factory_inputs.factory_placeholders,
        factory_copy_substrings=factory_inputs.factory_copy_substrings,
        xml_out_file=output_xml_path,
    )
    app_factory.make_copies_in_folders("ICG-L04M")
    app_factory.make_document(max_items_per_file=2)

    # Assert: Check that 8 files are created with the pattern output_1.xml, output_2.xml, etc.
    expected_files = []
    for i in range(1, 9):  # output_1.xml through output_8.xml
        expected_file = os.path.join(tmp_path, f"output_{i}.xml")
        expected_files.append(expected_file)
        assert os.path.exists(
            expected_file
        ), f"Output file {expected_file} does not exist"

    # Check that each file contains valid XML content and max 2 elements in ExportedObjects
    import xml.etree.ElementTree as ET

    for i, file_path in enumerate(expected_files):
        with open(file_path, "r", encoding="utf-8") as f:
            xml_content = f.read()
        assert (
            "<ObjectSet" in xml_content
        ), f"File {file_path} missing ObjectSet element"
        assert (
            "ExportedObjects" in xml_content
        ), f"File {file_path} missing ExportedObjects element"
        assert "Types" in xml_content, f"File {file_path} missing Types element"

        # Parse XML and check ExportedObjects element count
        try:
            root = ET.fromstring(xml_content)
            exported_objects = root.find("ExportedObjects")
            assert (
                exported_objects is not None
            ), f"File {file_path} missing ExportedObjects element"

            # Count child elements in ExportedObjects
            child_count = len(list(exported_objects))
            assert (
                child_count <= 2
            ), f"File {file_path} has {child_count} elements in ExportedObjects, expected max 2"
            assert (
                child_count > 0
            ), f"File {file_path} has no elements in ExportedObjects"

        except ET.ParseError as e:
            assert False, f"File {file_path} contains invalid XML: {e}"

    # Verify no extra files were created
    xml_files = [f for f in os.listdir(tmp_path) if f.endswith(".xml")]
    assert (
        len(xml_files) == 8
    ), f"Expected 8 XML files, but found {len(xml_files)}: {xml_files}"
