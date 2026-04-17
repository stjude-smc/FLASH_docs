FLASH documentation (Sphinx) — local build
==========================================

This directory is a Sphinx project. Built HTML is written to _build/html/ (ignored by git).

Prerequisites
-------------

- Python 3.9+ recommended.
- From the repository root (FLASH_doc/), create/activate a venv and install dependencies::

    source venv/bin/activate
    pip install -r docs_flash/requirements.txt

Regenerate .rst from Word
-------------------------

Source .docx files live under ../FLASH Documentation 20260417/

From the repository root::

    python import_doc1.py
    python import_doc2.py
    python import_doc3.py

Each script writes reStructuredText under docs_flash/rst/ and refreshes rst/_toctree_generated.rst.
Images are stored under docs_flash/_static/<doc_key>/.

Build HTML locally
------------------

From this directory (docs_flash/)::

    make html

Or::

    sphinx-build -b html . _build/html

Open _build/html/index.html in a browser.

If the build looks stale::

    make clean
    make html

Adding a new sidebar page (“tab”)
----------------------------------

The left-hand navigation follows the .. toctree:: directives. The master index includes
rst/_toctree_generated.rst, which is regenerated when you run the import scripts.

To add a page:

1. Add or generate a .rst file (for example under rst/).
2. Add its name without the .rst suffix to the appropriate .. toctree:: block (edit
   import_doc_common.TOCTREE_DOC_ORDER / regenerate_full_toctree logic, or extend the import
   pipeline for new Word sources).
3. Run make html again.

After you push to git (later)
-----------------------------

Publishing (Read the Docs, GitHub Pages, an internal server, etc.) can use the same sources
under docs_flash/ and a standard sphinx-build -b html step; hosting details are left for when
you choose a platform.
