import os
from ebo_app_factory.ebo_xml_builder import EBOXMLBuilder


def test_create_xml_with_folders(tmp_path):
    builder = EBOXMLBuilder(ebo_version="5.0.3.117")
    folder = builder.create_folder(name="Test Folder", description="Test Description")
    child_folder = builder.create_folder(
        name="Child Folder",
        description="Child Description",
        note1="Note1",
        note2="Note2",
    )
    folder.append(child_folder)

    builder.add_to_exported_objects(folder)
    xml_str = builder.to_pretty_xml()
    print(xml_str)
    # Basic checks
    output_path = os.path.join(tmp_path, "tmp_output.xml")
    builder.write_xml(output_path)
    assert os.path.exists(output_path), f"Output file {output_path} does not exist"
    with open(output_path, "r", encoding="utf-8") as f:
        xml_from_file = f.read()
    assert '<SourceVersion Value="5.0.3.117"/>' in xml_from_file
    assert (
        '<OI NAME="Test Folder" TYPE="system.base.Folder" DESCR="Test Description">'
        in xml_from_file
    )
    # TODO: assert the child folder is inside the parent folder
    assert (
        '<OI NAME="Child Folder" TYPE="system.base.Folder" DESCR="Child Description">'
        in xml_from_file
    )
    assert '<PI Name="NOTE1" Value="Note1"/>' in xml_from_file
    assert '<PI Name="NOTE2" Value="Note2"/>' in xml_from_file
