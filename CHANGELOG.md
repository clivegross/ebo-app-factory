# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.3.0] - 2025-07-11

### Added

- **New `EBOHTMLFileBuilder` class**: Complete support for creating HTML file objects and ObjectTypes for EBO import
- **HTML content compression and encoding**: Automatic gzip compression and Base64 encoding of HTML content for EBO compatibility
- **Version-specific UID generation**: Automatic selection of correct namespace based on EBO version (v5.0.3.117 vs v6.0.4.90+)
- **CDATA support for FileContents**: Proper CDATA wrapping of compressed HTML content in XML output
- **HTML compression utilities**: New `html_compression_utils.py` module with functions for HTML encoding/decoding
- **Schneider Electric UID generation**: Enhanced UID generation with content-based object IDs for HTML files

### Technical

- **EBO namespace compatibility**: Correctly handles different HTML file namespaces for different EBO versions
  - EBO v5.0.3.117: `udt.nulr4l2rmpbelizyq3aoiagyee`
  - EBO v6.0.4.90+: `udt.apsutrxlanbe5eerqx5ddeybmm`
- **Round-trip validation**: Full HTML content preservation through compression/decompression cycles
- **Content-based UIDs**: Deterministic UID generation based on HTML content for consistency
- **Comprehensive test coverage**: Complete test suite for HTML file builder functionality

### Fixed

- **UID format validation**: Resolved EBO import errors related to incorrect UID namespaces
- **XML structure compliance**: Ensures generated XML matches EBO import requirements exactly
- **EBOXMLBuilder object_types synchronization**: Fixed `object_types` to properly reference the Types element in the XML structure
- **Eliminated unnecessary XML operations**: Removed redundant remove/append operations in `add_to_exported_objects` method

## [0.2.1] - 2025-07-05

### Added

- Multi-file output support: `make_document()` now splits large datasets into multiple files based on `max_items_per_file` parameter
- Automatic file naming with sequential suffixes (`_1.xml`, `_2.xml`, etc.) when creating multiple files
- Enhanced test coverage for multi-file output validation

### Changed

- `make_document()` method now uses `set_exported_objects()` instead of `add_to_exported_objects()` to overwrite elements for multuple output file support
- Types elements are now added once per document set rather than per file
- Improved file generation logic to handle both single and multiple file scenarios

### Fixed

- Fixed file output naming to properly generate sequential files when `max_items_per_file` is specified
- Improved progress reporting for multi-file operations

### Technical

- Enhanced test suite to validate proper file splitting and XML element counting
- Better error handling for large dataset processing

## [0.2.0] - 2025-07-05

### Added

- New `ApplicationFactory` class `make_copies_in_folders()` method extends `make_copies()` method to put copies in specified EBO folders.
- Support for "Types" element in `EBOXMLBuilder` class with `add_object_type` method
- Support for mixed XML element types (minidom and ElementTree)
- Enhanced folder-based organization for exported objects
- Improved error handling for XML element conversion
- Type checking for XML elements before conversion
- Better whitespace handling in XML output

### Changed

- Refactored `ApplicationFactory` class to use the new `EBOXMLBuilder` class for building and writing XML.
- Improved XML element conversion between minidom and ElementTree formats
- Enhanced `ApplicationFactory` class with better document handling

### Fixed

- Refactored `ApplicationFactory` class `make_copies()` method to only copy ExportedObjects, leaving placeholder Types unchanged
- Fixed element appending between different XML document types using `importNode`

### Technical

- Added proper type checking for XML elements
- Improved memory efficiency by avoiding unnecessary conversions
- Enhanced debugging capabilities with better element inspection

## [0.1.6] - 2025-06-13

### Added

- Hyperlink support to `EBOXMLBuilder`

### Changed

- Updated documentation
- Improved README with better examples

## [0.1.5] - 2025-06-12

### Added

- EBO alarm and alarm view object support with `EBOAlarmBuilder`
- Change of state alarm support
- Sum alarm support
- Alarm view support

### Changed

- Updated documentation for alarm features

## [0.1.4] - 2025-06-12

### Added

- `create_folder` method for better folder organization
- Enhanced project metadata in `pyproject.toml`

### Changed

- Updated documentation with new folder creation examples

## [0.1.3] - 2025-06-04

### Added

- Enhanced XML building capabilities

### Changed

- Improved XML output formatting

## [0.1.2] - 2025-06-04

### Added

- `EBOXMLBuilder` for generic EBO-compliant exported objects XML
- `EBOModbusBuilder` for Modbus device, registers and register group objects
- `EBOScheduleBuilder` for EBO multistate time schedule objects
- Enhanced template processing capabilities

### Changed

- Improved Excel workbook processing
- Better error handling for template operations

## [0.1.0] - 2025-06-04

### Added

- Initial standalone release of `ebo-app-factory`
- Core `ApplicationFactoryManager` class
- Template-based XML generation
- Excel-driven placeholder replacement
- Support for EcoStruxure Building Operation XML formats
- Basic XML building utilities

### Features

- Build EBO applications from templates
- Mass produce EBO objects from Excel spreadsheets
- Support for placeholder replacement in XML templates
- EBO-compliant XML output for direct import
- Modular architecture with separate builders for different object types

## [0.0.1] - 2021-06-16

### Added

- **Initial Release**: Migrated `ebo_app_factory` module from [ebo-engineering-toolkit](https://github.com/SEBA-Smart-Services/ebo-engineering-toolkit)
- EBO Application Factory Manager
- EBO Application Factory core functionality
- Foundation for template-based EBO application generation

### Notes

- This release represents the migration of the original `ebo_app_factory` module from the SEBA Smart Services engineering toolkit
- Original development started June 16, 2021
- Established as standalone package for better maintainability and distribution

---

## Release Notes

### Version 0.2.0 Highlights

This release focuses on architectural improvements and better XML handling:

- **Improved Performance**: Only ExportedObjects are copied, Types remain unchanged
- **Better Compatibility**: Enhanced support for mixed XML element types
- **Cleaner Output**: Resolved blank line issues in generated XML
- **More Robust**: Better error handling and type checking

### Version 0.1.x Series

The 0.1.x series established the core functionality:

- Template-based application generation
- Excel integration for mass production
- Support for alarms, schedules, and Modbus devices
- Comprehensive XML building utilities

## Migration Guide

### From 0.1.x to 0.2.0

- No breaking changes in public API
- Improved performance with existing code
- Better error messages for troubleshooting

---

For more details about each release, see the [commit history](https://github.com/clivegross/ebo-app-factory/commits/main).
