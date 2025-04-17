#!/usr/bin/env python3
"""Generate SecureBootKeys.dsc.inc file from binary files."""

import argparse
import sys
from pathlib import Path


def bytes_to_c_array(data: bytes) -> str:
    """Convert bytes to a C-style array string."""
    return "{ " + ", ".join(f"0x{b:02X}" for b in data) + " }"


def main() -> None:
    """Generate SecureBootKeys.dsc.inc from binary files in the specified directory."""
    parser = argparse.ArgumentParser(
        description='Generate SecureBootKeys.dsc.inc from binary files'
    )
    parser.add_argument(
        'directory',
        type=str,
        help='Directory containing binary files and output location'
    )
    args = parser.parse_args()

    # Convert input to Path and ensure it exists
    work_dir = Path(args.directory)
    if not work_dir.is_dir():
        print(f"Error: Directory '{work_dir}' does not exist", file=sys.stderr)
        sys.exit(1)

    output_file = work_dir / "SecureBootKeys.dsc.inc"

    # Dictionary mapping bin files to their PCD names
    pcd_mapping = {
        "DefaultPk.bin": "PcdDefaultPk",
        "DefaultKek.bin": "PcdDefaultKek",
        "DefaultDb.bin": "PcdDefaultDb",
        "Default3PDb.bin": "PcdDefault3PDb",
        "DefaultDbx.bin": "PcdDefaultDbx"
    }

    # Start with the header
    content = "[PcdsFixedAtBuild.common]\n"

    # Process each .bin file
    for bin_file, pcd_name in pcd_mapping.items():
        bin_path = work_dir / bin_file
        if not bin_path.exists():
            print(f"Warning: {bin_file} not found", file=sys.stderr)
            continue

        with open(bin_path, 'rb') as f:
            data = f.read()

        # Add the PCD definition
        content += f"  gMsCorePkgTokenSpaceGuid.{pcd_name}|{bytes_to_c_array(data)}\n"

    # Write the output file
    with open(output_file, 'w') as f:
        f.write(content)

    print(f"Generated {output_file}")


if __name__ == "__main__":
    main()
