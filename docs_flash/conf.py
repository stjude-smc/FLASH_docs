# -*- coding: utf-8 -*-
# FLASH documentation — Sphinx configuration (local HTML builds).

import os
import sys

sys.path.insert(0, os.path.abspath("."))

extensions = [
    "sphinx.ext.mathjax",
]

templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = "FLASH"
copyright = "FLASH contributors"
author = "FLASH contributors"
version = "1.0"
release = "1.0"

language = "en"
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
pygments_style = "sphinx"

# Number figures so :numref: works for .. figure:: with :name:
numfig = True

html_theme = "sphinx_rtd_theme"
html_title = "FLASH documentation"
html_short_title = "FLASH"
html_static_path = ["_static"]
htmlhelp_basename = "FLASHdoc"
