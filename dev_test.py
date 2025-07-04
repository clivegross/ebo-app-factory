#!/usr/bin/env python3
"""
Development testing script for quick iteration
"""
import os
import sys
import xml.etree.ElementTree as ET

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "src"))

from ebo_app_factory.xml_app_factory import (
    ApplicationFactory,
    ApplicationTemplate,
    FactoryInputsFromSpreadsheet,
)


def main():
    """Main development testing function"""
    print("=== Development Testing Script ===")

    # Test your new classes or functions here
    print("\nTesting ApplicationTemplate...")

    # Example: Create an instance and print its attributes
    test_dir = os.path.dirname(__file__)
    item_workbook_path = os.path.join(test_dir, "tests", "data", "items.xlsx")
    template_file = os.path.join(
        test_dir,
        "tests",
        "data",
        "Emergency Lighting Group ICG-L04M EBO app Export 2024-04-19.xml",
    )
    xml_out_file = os.path.join(test_dir, "tests", "data", "output.xml")

    if os.path.exists(template_file):
        # Use a real template file
        try:
            app_template = ApplicationTemplate(
                template_file,
                print_result=True,
            )

            print("ApplicationTemplate created successfully!")
            print("Attributes:")
            for key, value in vars(app_template).items():
                print(f"  {key}: {type(value).__name__} = {value}")

        except Exception as e:
            print(f"Error creating ApplicationTemplate: {e}")
    else:
        print(f"Test file not found: {template_file}")

    print("\n\nTesting FactoryInputsFromSpreadsheet...")

    # Example: Create an instance and print its attributes

    if os.path.exists(item_workbook_path):
        # Use a real spreadsheet file

        try:
            factory_inputs = FactoryInputsFromSpreadsheet(
                item_workbook_path, print_result=True
            )

            print("FactoryInputsFromSpreadsheet created successfully!")
            print("Attributes:")
            for key, value in vars(factory_inputs).items():
                print(f"  {key}: {type(value).__name__} = {value}")

        except Exception as e:
            print(f"Error creating FactoryInputsFromSpreadsheet: {e}")
    else:
        print(f"Test file not found: {item_workbook_path}")

    print("\n\nTesting ApplicationFactory...")

    if os.path.exists(template_file) and os.path.exists(item_workbook_path):
        print("Create ApplicationFactory...")
        try:
            app_factory = ApplicationFactory(
                template_child_elements_dict=app_template.template_child_elements_dict,
                factory_placeholders=factory_inputs.factory_placeholders,
                factory_copy_substrings=factory_inputs.factory_copy_substrings,
                xml_out_file=xml_out_file,
            )
            print("ApplicationFactory created successfully!")
            print("Attributes:")
            for key, value in vars(app_factory).items():
                print(f"  {key}: {type(value).__name__} = {value}")

            def print_element_lines(element, num_lines=20):
                """Print first N lines of a DOM element"""
                xml_string = element.toprettyxml(indent="  ")
                lines = [line for line in xml_string.split("\n") if line.strip()]
                for i, line in enumerate(lines[:num_lines]):
                    print(f"{i+1:2d}: {line}")

            # Print first 20 lines of each element in the dict
            # for key, elements_list in app_factory.template_child_elements_dict.items():
            #     print(f"\n=== {key} ===")
            #     for idx, element in enumerate(elements_list):
            #         if len(elements_list) > 1:
            #             print(f"\n--- Element {idx+1} ---")
            #         print_element_lines(element, 20)
            #         print()  # Add blank line between elements

            app_factory.make_copies_in_folders("ICG-L04M")
            app_factory.make_document(
                write_result=True, print_result=False, max_items_per_file=2
            )

            # app_factory.make_copies()
            # print("Copies made successfully!")
            # print("Factory Copies Dictionary:")
            # print(app_factory.factory_copies_dict)
            # for idx, element in enumerate(
            #     app_factory.factory_copies_dict["ExportedObjects"]
            # ):
            #     print(f"\n=== ExportedObjects Item {idx+1} ===")
            #     lines = [
            #         line
            #         for line in element.toprettyxml(indent="  ").split("\n")
            #         if line.strip()
            #     ]
            #     for i, line in enumerate(lines[:3]):
            #         print(f"{i+1:2d}: {line}")
            #     print()

            # app_factory.make_document(write_result=True, print_result=False)

        except Exception as e:
            print(f"Error creating ApplicationFactory: {e}")

    print("=== End Testing ===")


if __name__ == "__main__":
    main()
