:orphan:

.. _placeholder:

Documentation sources not generated yet
========================================

The main table of contents is produced by the import scripts. From the repository root, with
your virtualenv activated::

   source venv/bin/activate
   pip install -r docs_flash/requirements.txt
   python import_doc1.py
   python import_doc2.py
   python import_doc3.py

Then build HTML::

   cd docs_flash
   make html

Open ``_build/html/index.html`` in a browser.
