#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Import FLASH Documentation.docx into docs_flash/rst/."""
from __future__ import annotations

import argparse
from pathlib import Path

from import_doc_common import convert_docx_to_rst_tree, regenerate_full_toctree

REPO = Path(__file__).resolve().parent
DOC_DIR = REPO / "FLASH Documentation 20260417"
DEFAULT_DOCX = DOC_DIR / "FLASH Documentation.docx"
MANUAL_IMAGES = DOC_DIR / "manual images"


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--out",
        type=Path,
        default=REPO / "docs_flash",
        help="Sphinx source root (default: ./docs_flash)",
    )
    ap.add_argument(
        "--docx",
        type=Path,
        default=DEFAULT_DOCX,
        help="Path to the .docx file",
    )
    args = ap.parse_args()
    out = args.out.resolve()
    convert_docx_to_rst_tree(
        args.docx.resolve(),
        out,
        "flash_documentation",
        doc_title="FLASH Documentation",
        copy_manual_images=MANUAL_IMAGES if MANUAL_IMAGES.is_dir() else None,
    )
    regenerate_full_toctree(out)
    print(f"Wrote RST under {out / 'rst'}; manifest {out / 'manifest_flash_documentation.json'}")


if __name__ == "__main__":
    main()
