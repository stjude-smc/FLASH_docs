FLASH documentation (Sphinx)
============================

This directory is the Sphinx source tree for FLASH documentation.
Built HTML is written to _build/html/ and is not committed to git.

Repository: https://github.com/stjude-smc/FLASH_docs

Published site (GitHub Pages)
------------------------------

When GitHub Pages and the deploy workflow are enabled on the repository:

  https://stjude-smc.github.io/FLASH_docs/

Sphinx html_baseurl in conf.py is set to that URL so links and static assets
work on Pages.

What belongs in git
-------------------

Commit (sources):

  index.rst, _toctree_generated.rst, rst/*.rst, _static/, conf.py, Makefile,
  requirements.txt

Do not commit (build output):

  docs_flash/_build/

The .rst under docs_flash/rst/ must be tracked for CI and GitHub Pages to build
a complete site. Only docs_flash/_build/ should stay ignored.

Editing policy
--------------

The master index.rst states that import scripts should not be re-run casually:
outputs were edited manually. For content changes, edit the .rst files under
rst/ directly, then rebuild HTML.

Regenerate .rst from Word (optional, destructive)
-------------------------------------------------

Source .docx files live under ../FLASH Documentation 20260417/ (local; ignored by git).

From the repository root::

    python import_doc1.py
    python import_doc2.py
    python import_doc3.py

Each script writes reStructuredText under docs_flash/rst/ and refreshes
_toctree_generated.rst. Images go under docs_flash/_static/<doc_key>/.

Only run these if you intend to overwrite generated .rst from Word.

Prerequisites
-------------

- Python 3.9+ recommended.
- From the repository root, create/activate a venv and install dependencies::

    source venv/bin/activate
    pip install -r docs_flash/requirements.txt

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

After you change any .rst file::

    cd docs_flash && make clean && make html

Adding a new sidebar page ("tab")
---------------------------------

The left-hand navigation follows .. toctree:: directives. The master index
includes _toctree_generated.rst (regenerated when you run the import scripts).

To add a page:

1. Add or generate a .rst file (for example under rst/).
2. Add its name without the .rst suffix to the appropriate .. toctree:: block
   (edit import_doc_common.TOCTREE_DOC_ORDER / regenerate logic, or extend the
   import pipeline for new Word sources).
3. Run make html again.

Publishing with GitHub Actions
------------------------------

Workflow file (in the repository):

  .github/workflows/deploy-documentation.yml

GitHub only runs workflows under .github/workflows/ (plural). If the file still
lives under .github/workflow/, move it before expecting Actions to run.

The workflow "Deploy Documentation to GitHub Pages":

  - Triggers on push to main, or manual run (workflow_dispatch)
  - Installs docs_flash/requirements.txt
  - Runs: sphinx-build -b html docs_flash docs_flash/_build/html
  - Deploys the HTML artifact via GitHub Pages (Actions source)

One-time setup on GitHub (repo or fork):

  Settings -> Pages -> Build and deployment -> Source: GitHub Actions

First deploy may require approving the github-pages environment on org repos.

Admonitions (sphinx_rtd_theme callouts)
---------------------------------------

Directive         Typical use (semantics)
.. attention::     Something the reader must notice
.. caution::      Possible problem if ignored
.. danger::       Risk of harm or loss of data
.. error::        Error / failed state
.. hint::         Helpful but non-obvious tip
.. important::     Critical information
.. note::         Extra note (often blue in RTD)
.. tip::          Suggestion / best practice
.. warning::      Strong caution (often amber/orange in RTD)

Repository root README
----------------------

A short README.md at the repository root (if added) should link to the published
site, local build steps above, and this file for author details.