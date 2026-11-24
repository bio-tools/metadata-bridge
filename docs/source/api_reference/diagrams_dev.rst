Process diagrams
================

General flow
------------

This sequence diagram illustrates the high-level runtime flow of the GitHub ⇄ bio.tools bridge.
It shows how user input is handled by the interface, routed through the central handler, and executed
depending on the selected direction of the bridge.

.. mermaid:: _process_diagrams/bridge-flow.mmd


Composing models
-----------------

The sequence diagram below details the process of composing the metadata models
from GitHub repositories and bio.tools entries.

.. mermaid:: _process_diagrams/composing.mmd


GitHub → bio.tools pipeline
----------------------------

The sequence diagram below details the pipeline for mapping GitHub repository
to a bio.tools tool metadata.

.. mermaid:: _process_diagrams/gh2bt.mmd


bio.tools → GitHub pipeline
----------------------------

The sequence diagram below details the pipeline for mapping a bio.tools tool
metadata to a GitHub repository in the form of a pull request and, optionally,
issues.

.. mermaid:: _process_diagrams/bt2gh.mmd


Reconciliation policies
------------------------

The flowcharts below show how a mapped value is combined with the value already present
on the other side. They are generic and shared by many of the field-specific map functions.

Policy: GitHub over bio.tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid:: _process_diagrams/gh2bt/policy-gh-over-bt.mmd

Policy: bio.tools over GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid:: _process_diagrams/bt2gh/policy-bt-over-gh.mmd

Policy: bio.tools on top of GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. mermaid:: _process_diagrams/bt2gh/policy-bt-ontop-gh.mmd
