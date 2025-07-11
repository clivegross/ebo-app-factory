#!/usr/bin/env python3
"""
Schneider Electric Building Operation Unique Identifier Generator

Generates UIDs in the format: prefix.namespace_id.object_id
Example: udt.apsutrxlanbe5eerqx5ddeybmm.ubsvymz6thv3uo6sr3ieghdenw2d52hd
"""

import base64
import hashlib
import secrets
import time
import argparse


def base32_encode_custom(data: bytes) -> str:
    """
    Custom base32 encoding using lowercase letters (similar to Schneider Electric format).
    """
    encoded = base64.b32encode(data).decode("ascii").lower().rstrip("=")
    return encoded


def generate_schneider_uid(
    prefix: str = "udt", namespace_seed: str = None, object_seed: str = None
) -> str:
    """
    Generate a Schneider Electric Building Operation style unique identifier.

    Args:
        prefix (str): Type prefix (e.g., "udt", "sys", "client")
        namespace_seed (str): Optional seed for reproducible namespace ID
        object_seed (str): Optional seed for reproducible object ID

    Returns:
        str: Generated unique identifier
    """
    # Generate namespace ID (~26 characters)
    if namespace_seed:
        namespace_hash = hashlib.sha256(namespace_seed.encode()).digest()
    else:
        namespace_data = f"user_{time.time()}_{secrets.token_hex(8)}".encode()
        namespace_hash = hashlib.sha256(namespace_data).digest()

    namespace_id = base32_encode_custom(namespace_hash[:16])

    # Generate object ID (~32 characters)
    if object_seed:
        object_hash = hashlib.sha256(object_seed.encode()).digest()
    else:
        object_data = f"obj_{time.time()}_{secrets.token_hex(12)}".encode()
        object_hash = hashlib.sha256(object_data).digest()

    object_id = base32_encode_custom(object_hash[:20])

    return f"{prefix}.{namespace_id}.{object_id}"


def generate_content_based_uid(html_content: str, prefix: str = "udt") -> str:
    """
    Generate a content-based UID for HTML files that EBO can validate.
    This creates a UID where the object ID is derived from the HTML content hash.

    Args:
        html_content (str): HTML content to hash
        prefix (str): Type prefix (e.g., "udt", "sys", "client")

    Returns:
        str: Content-based unique identifier
    """
    # Create a consistent namespace for HTML content
    namespace_data = "html_content_namespace".encode()
    namespace_hash = hashlib.sha256(namespace_data).digest()
    namespace_id = base32_encode_custom(namespace_hash[:16])

    # Generate object ID based on HTML content
    content_hash = hashlib.sha256(html_content.encode("utf-8")).digest()
    object_id = base32_encode_custom(content_hash[:20])

    return f"{prefix}.{namespace_id}.{object_id}"


def generate_html_file_uid(
    html_content: str, prefix: str = "udt", ebo_version: str = "6.0.4.90"
) -> str:
    """
    Generate a UID specifically for HTML files using the fixed namespace that EBO expects.
    Based on analysis of EBO exports, different versions use different namespaces:
    - EBO v6.0.4.90+: udt.apsutrxlanbe5eerqx5ddeybmm
    - EBO v5.0.3.117: udt.nulr4l2rmpbelizyq3aoiagyee

    Args:
        html_content (str): HTML content to hash for the object ID
        prefix (str): Type prefix (e.g., "udt")
        ebo_version (str): EBO version to determine correct namespace

    Returns:
        str: HTML file UID with version-specific namespace and content-based object ID
    """
    # Choose namespace based on EBO version
    if ebo_version.startswith("5.0.3"):
        namespace_id = "nulr4l2rmpbelizyq3aoiagyee"  # EBO v5.0.3.117
    else:
        namespace_id = "apsutrxlanbe5eerqx5ddeybmm"  # EBO v6.0.4.90+

    # Generate object ID based on HTML content
    content_hash = hashlib.sha256(html_content.encode("utf-8")).digest()
    object_id = base32_encode_custom(content_hash[:20])

    return f"{prefix}.{namespace_id}.{object_id}"


def main():
    parser = argparse.ArgumentParser(
        description="Generate Schneider Electric Building Operation UIDs"
    )
    parser.add_argument("--prefix", default="udt", help="Type prefix (default: udt)")
    parser.add_argument(
        "--namespace", help="Namespace seed for reproducible namespace ID"
    )
    parser.add_argument("--object", help="Object seed for reproducible object ID")
    parser.add_argument(
        "--count", type=int, default=1, help="Number of UIDs to generate"
    )
    parser.add_argument(
        "--project", help="Project name (used with --name for reproducible UIDs)"
    )
    parser.add_argument(
        "--name", help="Object name (used with --project for reproducible UIDs)"
    )

    args = parser.parse_args()

    if args.project and args.name:
        # Generate reproducible UID based on project and object name
        namespace_seed = f"project_{args.project}"
        object_seed = f"object_{args.name}_{args.project}"
        uid = generate_schneider_uid(args.prefix, namespace_seed, object_seed)
        print(f"Project: {args.project}")
        print(f"Object:  {args.name}")
        print(f"UID:     {uid}")
    else:
        # Generate specified number of UIDs
        for i in range(args.count):
            uid = generate_schneider_uid(args.prefix, args.namespace, args.object)
            if args.count == 1:
                print(uid)
            else:
                print(f"{i+1:2}. {uid}")


if __name__ == "__main__":
    main()
