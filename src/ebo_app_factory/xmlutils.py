# Import the required library
from xml.dom import minidom
import xml.etree.ElementTree as ET
import re
import csv


def find_elements_in_xml(file_path, element_name=None, attributes=None):
    """
    Reads an XML file and returns a list of all the elements inside a specified element.
    The specified element can be found using arguments for element name and/or element attributes.

    :param file_path: Path to the XML file
    :param element_name: Name of the element to find (optional)
    :param attributes: Dictionary of attributes to match (optional)
    :return: List of found elements
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    # If no element name and attributes are provided, return all elements
    if not element_name and not attributes:
        return [elem for elem in root.iter()]

    found_elements = []

    # Iterate through all elements in the XML
    for elem in root.iter():
        # Check if the current element matches the specified name
        if element_name and elem.tag != element_name:
            continue

        # If attributes are specified, check if the current element matches all the specified attributes
        if attributes:
            attribute_match = all(
                elem.get(attr) == value for attr, value in attributes.items()
            )
            if not attribute_match:
                continue

        # If the element matches the criteria, add it to the list
        found_elements.append(elem)

    return found_elements


def find_child_elements_in_xml(
    file_path, parent_element_name=None, parent_attributes=None
):
    """
    Reads an XML file and returns a list of all child elements of a specified parent element.
    The parent element can be found using arguments for element name and/or element attributes.

    :param file_path: Path to the XML file
    :param parent_element_name: Name of the parent element to find (optional)
    :param parent_attributes: Dictionary of attributes to match for the parent element (optional)
    :return: List of child elements of the found parent element(s)
    """
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()

    child_elements = []

    # Define a function to check if an element matches the given criteria
    def element_matches_criteria(element, name, attributes):
        if name and element.tag != name:
            return False
        if attributes:
            for attr, value in attributes.items():
                if element.get(attr) != value:
                    return False
        return True

    # Iterate through all elements in the XML
    for elem in root.iter():
        # Check if the current element matches the specified parent criteria
        if element_matches_criteria(elem, parent_element_name, parent_attributes):
            # Add all child elements of the matching parent element to the list
            for child in elem:
                child_elements.append(child)

    return child_elements


def build_parent_map(tree):
    parent_map = {c: p for p in tree.iter() for c in p}
    return parent_map


def find_child_elements_in_folder(file_path, folder_name=None):
    # parent_element_name='OI', parent_attributes={'TYPE': 'system.base.Folder', 'NAME': 'Variables'}
    tree = ET.parse(file_path)

    child_elements = find_child_elements_in_xml(
        file_path,
        parent_element_name="OI",
        parent_attributes={"TYPE": "system.base.Folder", "NAME": folder_name},
    )
    modified_child_elements = []

    for child in child_elements:
        child_copy = ET.Element(child.tag, child.attrib)
        child_copy.attrib["FOLDER"] = folder_name
        modified_child_elements.append(child_copy)

    return modified_child_elements


def find_elements_in_folders(file_path, folder_names):
    """
    Finds and returns elements from specified folders within an XML file.

    This function searches for child elements within specified folders by their names in an XML file. It handles both single folder names and lists of folder names. For each folder specified, it finds child elements that match the criteria and returns a combined list of these elements.

    Parameters:
    - file_path (str): The path to the XML file to be searched.
    - folder_names (Union[str, List[str]]): A single folder name or a list of folder names within the XML file from which to find child elements.

    Returns:
    - List[ET.Element]: A list of ElementTree.Element objects representing the found child elements within the specified folders.
    """
    # Check if folder_names is a string and convert it to a list if so
    if isinstance(folder_names, str):
        folder_names = [folder_names]
    all_elements = []
    for folder_name in folder_names:
        elements = find_child_elements_in_folder(file_path, folder_name)
        all_elements.extend(elements)
    return all_elements


def write_elements_to_csv(elements, csv_file_path, attributes=None):
    """
    Writes a list of XML elements and their attributes to a CSV file with specified columns.
    If attributes is None, all attributes found in the elements will be used as columns.

    Parameters:
    - elements (List[Element]): A list of XML Element objects.
    - csv_file_path (str): The path to the CSV file to be written.
    - attributes (List[str] | None): A list of attribute names to be written as columns in the CSV file, or None to write all attributes.
    """
    if attributes is None:
        # Find all unique attribute names across all elements
        all_attributes = set()
        for elem in elements:
            all_attributes.update(elem.attrib.keys())
        headers = list(all_attributes)
    else:
        headers = attributes

    with open(csv_file_path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(headers)  # Write the header row

        for elem in elements:
            # Extract attributes with a default of '' if not found
            row = [elem.get(attr, "") for attr in headers]

            writer.writerow(row)  # Write the element's attributes as a row


def clean_elements(elements, attributes_to_keep=None, remove_duplicates=True):
    """
    Returns a list of XML elements and their attributes.
    If attributes_to_keep is None, all attributes found in the elements will be returned.
    If attributes_to_keep is provided, only those attributes will be returned.
    Removes duplicates if remove_duplicates is True based on the specified attributes.

    Parameters:
    - elements (List[Element]): A list of XML Element objects.
    - attributes_to_keep (List[str] | None): A list of attribute names to be included in elements in the returned list.
    - remove_duplicates (bool): Whether to remove duplicate rows based on attributes.
    """
    if attributes_to_keep is None:
        # Find all unique attribute names across all elements
        all_attributes = set()
        for elem in elements:
            all_attributes.update(elem.attrib.keys())
        headers = list(all_attributes)
    else:
        headers = attributes_to_keep

    seen = set()  # To track unique attribute combinations

    cleaned_elements = []

    for elem in elements:
        # Copy element and only keep specified attributes
        elem_copy = ET.Element(elem.tag, elem.attrib)
        for attr in list(elem_copy.attrib.keys()):
            if attr not in headers:
                del elem_copy.attrib[attr]
        cleaned_elements.append(elem_copy)

        if remove_duplicates:
            # Skip adding if this combination of attributes has been seen
            row = tuple(elem_copy.get(attr, "") for attr in headers)
            if row in seen:
                cleaned_elements.pop()
            else:
                seen.add(row)

    return cleaned_elements


def find_and_clean_folder_elements(
    xml_file_path,
    folder_names=["Variables", "Alarms", "Setpoints"],
    attributes=["NAME", "DESCR", "TYPE", "FOLDER"],
):
    """
    Finds child elements within specified folders in an XML file, cleans them, and returns them as a list of elements.

    Parameters:
    - xml_file_path (str): The path to the XML file.
    - folder_names (Union[str, List[str]]): A single folder name or a list of folder names within the XML file.
    - attributes (List[str]): A list of attribute names to keep in the cleaned elements.

    Returns:
    - List[ET.Element]: A list of cleaned ElementTree.Element objects representing the found child elements within the specified folders.
    """
    # Find elements in the specified folders
    elements = find_elements_in_folders(xml_file_path, folder_names)
    print(f"Found {len(elements)} child elements in the folders")

    # Clean the elements and return the cleaned list
    cleaned_elements = clean_elements(elements, attributes)
    return cleaned_elements


def export_folder_elements_to_csv(
    xml_file_path,
    folder_names=["Variables", "Alarms", "Setpoints"],
    attributes=["NAME", "DESCR", "TYPE", "FOLDER"],
    csv_file_path=None,
):
    """
    Finds child elements within specified folders in an XML file and writes their attributes to a CSV file.

    Parameters:
    - xml_file_path (str): The path to the XML file.
    - folder_names (Union[str, List[str]]): A single folder name or a list of folder names within the XML file.
    - csv_file_path (str): The path to the CSV file to be written.
    """
    # Ensure folder_names is a list
    if isinstance(folder_names, str):
        folder_names = [folder_names]

    # Find elements in the specified folders
    elements = find_and_clean_folder_elements(xml_file_path, folder_names, attributes)
    print(f"Found {len(elements)} child elements in the folders")

    # If no CSV file path is provided, use the XML file path with a .csv extension
    if csv_file_path is None:
        csv_file_path = xml_file_path + ".csv"

    # Write the elements and their attributes to the CSV file
    write_elements_to_csv(elements, csv_file_path)


def extract_mustache_tags_from_xml(xml_file_path):
    """
    Extracts a list of unique mustache tags from an XML file.

    Parameters:
    - xml_file_path (str): The path to the XML file.

    Returns:
    - List[str]: A list of unique mustache tags found in the file.
    """
    # Regular expression to find mustache tags
    mustache_tag_pattern = r"{{(.*?)}}"

    # Read the content of the XML file
    with open(xml_file_path, "r", encoding="utf-8") as file:
        file_content = file.read()

    # Find all occurrences of mustache tags
    found_tags = re.findall(mustache_tag_pattern, file_content)

    # Remove duplicates by converting the list to a set, then back to a list
    unique_tags = list(set(found_tags))

    return unique_tags


def to_pretty_xml(obj):
    """
    Converts the XML object to a pretty-printed string.
    Returns:
        str: Pretty-printed XML string.
    """
    rough = ET.tostring(obj, "utf-8")
    return minidom.parseString(rough).toprettyxml(indent="  ")


def print_pretty_xml(obj):
    """
    Converts the XML object to a pretty-printed string.
    Returns:
        str: Pretty-printed XML string.
    """
    print(to_pretty_xml(obj))
