import os
from ebo_app_factory.xml_app_factory import ApplicationFactoryManager


def test_application_factory_creates_xml(tmp_path):
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
