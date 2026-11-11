import pathlib
import sys
sys.path.insert(0, pathlib.Path(__file__).parents[2].resolve().as_posix())

# biscuit_auth is a compiled module, so autodoc can't find its source by itself.
# Point it to the type stub, so that `#:` comments there are used as documentation.
from sphinx.pycode import ModuleAnalyzer # type: ignore[import-not-found]

_stub_path = (pathlib.Path(__file__).parents[1] / "biscuit_auth.pyi").as_posix()
_for_module = ModuleAnalyzer.for_module

def _for_module_with_stub(modname):
    if modname == "biscuit_auth":
        return ModuleAnalyzer.for_file(_stub_path, modname)
    return _for_module(modname)

ModuleAnalyzer.for_module = _for_module_with_stub # type: ignore[method-assign]

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'biscuit-python'
copyright = '2023, Clément Delafargue'
author = 'Clément Delafargue'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc'
]

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']
