import os
import sys
from datetime import date
from pathlib import Path
import tomllib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../src")))

# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information


pyproject = Path(__file__).parent.parent.parent / "pyproject.toml"
with open(pyproject, "rb") as f:
    data = tomllib.load(f)

# extract metadata
project_meta = data.get("project", {})

project = project_meta.get("name", "Unknown Project")
author = ", ".join(a.get("name") for a in project_meta.get("authors", []) if a.get("name"))
version = project_meta.get("version", "0.0.0")
copyright = f"2025-{date.today().year}, {author}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",  # Automatically document your code from docstrings
    "sphinx.ext.napoleon",  # Support for NumPy and Google style docstrings
    "sphinx.ext.autosummary",  # Generate summary tables for modules/classes/functions
    "sphinx_autodoc_typehints",  # Use type hints for function signatures
    "sphinx.ext.viewcode",  # Add links to highlighted source code,
    "sphinx.ext.intersphinx",  # Link types to the Python and pydantic docs
    "myst_parser",  # Markdown parser
    "sphinx_automodapi.automodapi",  # Advanced autodoc for modules
    "sphinx_automodapi.smart_resolver",  # Better cross-referencing
    "sphinxcontrib.mermaid",  # Mermaid diagrams
]
napoleon_google_docstring = True
napoleon_numpy_docstring = True
myst_heading_anchors = 3  # lets Markdown pages link to headings, e.g. deployment_guide.md#docker
myst_enable_extensions = [
    "dollarmath",  # Enables $...$ syntax
    "amsmath",  # Enables LaTeX-style math blocks with \[ \] and environments
]

# https://sphinx-themed.readthedocs.io/en/latest/usage/extensions/autodoc.html
autodoc_default_options = {
    "autosummary": True,
    "members": True,
    "undoc-members": True,
    "private-members": False,
    "inherited-members": False,
    "show-inheritance": True,
    # "ignore-module-all": False,
    # "special-members": "__init__",
    "exclude-members": "model_config, model_fields, model_computed_fields",
    # "exclude-members": (
    #     # generic dunder methods
    #     "__weakref__,__repr__,__str__,__eq__,__hash__,__dict__,__slots__,__signature__,"
    #     "__setstate__,__getstate__,__reduce__,__reduce_ex__,__module__,__annotations__,"
    #     "__class__,__module__,"
    #     # some pydantic internal stuff (BaseModel/RootModel)
    #     "__pydantic_*,"
    #     "_abc_impl,_repr_*,"  # repr internals
    #     "_calculate_keys,_copy_and_set_values,_get_value,_iter,_setattr_handler,"
    #     "construct,copy,dict,from_orm,json,"
    #     "model_*,root,"
    #     "parse_file,parse_obj,parse_raw,"
    #     "schema,schema_json,"
    #     "validate,update_forward_refs,model_validate*,model_dump*,model_json_schema,"
    # ),
    "autoclass_content": "both",
    "autodoc_member_order": "bysource",
}

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "pydantic": ("https://pydantic.dev/docs/validation/latest", None),
}

suppress_warnings = []
autodoc_warningiserror = False
nitpicky = False

autoclass_content = "class"
napoleon_use_param = True  # Keep Parameters: parsed properly
napoleon_use_ivar = False  # Don't duplicate with autodoc attributes
napoleon_attr_annotations = False  # Merge type hints into the same table

autodoc_class_signature = "mixed"
autosummary_generate = True
autosummary_generate_overwrite = False  # keep the apidoc pages instead of replacing them with stubs
automodapi_toctreedirnm = "_generated"
autosummary_imported_members = False
autodoc_typehints = "description"
automodsumm_inherited_members = False
automodsumm_imported_members = False

mermaid_d3_zoom = True
mermaid_fullscreen = True

templates_path = ["_templates"]
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "sphinx_book_theme"

html_theme_options = {
    "repository_url": "https://github.com/bio-tools/metadata-bridge",
    "use_repository_button": True,
    "use_issues_button": True,
    "use_edit_page_button": True,
    "repository_branch": "dev",
    "path_to_docs": "docs/source",
    "navigation_depth": 10,
}


# -- Setup


def skip_enum_members(app, what, name, obj, skip, options):
    """Skip documenting Enum members automatically."""
    from enum import Enum

    if isinstance(obj, Enum):
        return True  # skip actual enum values like LanguageEnum.Python
    return skip


def skip_pydantic_internals(app, what, name, obj, skip, options):
    """Skip autogenerated Pydantic v2 internals like model_config and model_fields."""
    # Skip common Pydantic internal attributes
    if name in {"model_config", "model_fields", "model_computed_fields"}:
        return True

    # Skip Pydantic BaseModel class variables and internal methods
    if getattr(obj, "__module__", "").startswith("pydantic"):
        return True

    return skip


def run_apidoc(app, config=None):
    """Generate the developer API pages before Sphinx collects source files, so automodapi sees them."""
    import sphinx.ext.apidoc as apidoc
    import shutil

    root = Path(__file__).resolve().parents[2]  # <project-root>
    src_dir = root / "src" / "bridge"  # <project-root>/src/bridge
    out_dir = (
        Path(__file__).resolve().parent / "api_reference" / "_apidoc_generated"
    )  # docs/source/api_reference/_apidoc_generated
    tmpl_dir = root / "docs" / "_apidoc_templates"

    if not src_dir.exists():
        print(f"Source directory {src_dir} does not exist, skipping apidoc.")
        return

    if out_dir.exists():
        shutil.rmtree(out_dir)

    apidoc.main(
        [
            "-o",
            str(out_dir),
            str(src_dir),
            "-t",
            str(tmpl_dir),
            "--force",
            "--separate",
            "--module-first",
            "--implicit-namespaces",
            "--no-toc",  # index_dev.rst links the package pages; no extra modules.rst
        ]
    )


# pages generated at build time (or included from elsewhere) have no source file to edit
_PAGES_WITHOUT_SOURCE = ("_generated/", "api_reference/_apidoc_generated/", "changelog")


def hide_edit_button_on_generated_pages(app, pagename, templatename, context, doctree):
    """Hide the "Edit this page" button on pages that don't exist as files in docs/source."""
    if not pagename.startswith(_PAGES_WITHOUT_SOURCE):
        return

    def without_edit(buttons):
        kept = []
        for button in buttons:
            if "/edit/" in str(button.get("url", "")):
                continue
            if isinstance(button.get("buttons"), list):
                button = {**button, "buttons": without_edit(button["buttons"])}
            kept.append(button)
        return kept

    context["header_buttons"] = without_edit(context.get("header_buttons", []))


def setup(app):
    # runs after sphinx-book-theme adds its header buttons (priority 501)
    app.connect("html-page-context", hide_edit_button_on_generated_pages, priority=600)
    app.connect("autodoc-skip-member", skip_enum_members)
    app.connect("autodoc-skip-member", skip_pydantic_internals)
    app.connect("config-inited", run_apidoc)
