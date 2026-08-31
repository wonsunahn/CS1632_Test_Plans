# conf.py -- Sphinx + Sphinx-Needs skeleton for the CS 1632 traceability assignment.
# Students never edit this file; they only add .. req:: and .. test:: blocks
# in requirements.rst and test_plan.rst, then run one build command.

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning, module="sphinx_needs")

project = "POTUS"
author = "Wonsun Ahn"
release = "1.0"

extensions = ["sphinx_needs"]

# ---- Sphinx-Needs configuration -------------------------------------------

# Define custom need types to describe nodes.
needs_types = [
    dict(directive="proj", title="Project",        prefix="PROJ_", color="#B3C5D7", style="node"),
    dict(directive="req",  title="Requirement",    prefix="REQ_",  color="#BFD8D2", style="node"),
    dict(directive="spec", title="Specification",  prefix="SPEC_",  color="#FEDCD2", style="node"),
    dict(directive="impl", title="Implementation", prefix="IMPL_", color="#DF744A", style="node"),
    dict(directive="test", title="Test Case",      prefix="TEST_",   color="#DCB239", style="node"),
]

# Define custom link types to describe relationships.
needs_links = {
    "requiredby": {"incoming": "requires", "outgoing": "required by"},
    "specifies":  {"incoming": "specified by", "outgoing": "specifies"},
    "tests":      {"incoming": "tested by", "outgoing": "tests"},
}

# Force every requirement and test to carry an explicit, well-formed ID.
# e.g. PROJ_001 (project), REQ_001 (requirement), SPEC_001 (specification) or TEST_001 (test case).
needs_id_required = True
needs_id_regex = r"^(PROJ|REQ|SPEC|TEST)_[0-9]{3}$|^TEST_(EXPLICIT_BOUNDARY|IMPLICIT_BOUNDARY)$"
needs_warnings = {
    "proj_must_be_PROJ":  "type == 'proj'  and not id.startswith('PROJ_')",
    "req_must_be_REQ":  "type == 'req'  and not id.startswith('REQ_')",
    "spec_must_be_SPEC":  "type == 'spec'  and not id.startswith('SPEC_')",
    "test_must_be_TEST":  "type == 'test' and not id.startswith('TEST_')",
    "req_must_be_specified": "type == 'req' and len(specifies_back) == 0",
    "spec_must_be_covered": "type == 'spec' and len(tests_back) == 0",
    "test_must_not_be_orphaned": "type == 'test' and len(tests) == 0",
}

# Emit needs.json next to the HTML output so make_grid.py can build the
# requirements x tests grid from it. Lands at _build/html/needs.json.
needs_build_json = True

# Use graphviz to render the requirement-test traceability graph.
needs_flow_engine = "graphviz"
needs_graphviz_styles = {
    "lefttoright": {
        "graph": {"rankdir": "LR", "bgcolor": "transparent"},
        "node":  {"fontname": "sans-serif", "fontsize": 12},
        "edge":  {"color": "#57ACDC", "fontsize": 10},
    }
}

# alabaster ships with Sphinx, so no extra theme dependency.
html_theme = "alabaster"
