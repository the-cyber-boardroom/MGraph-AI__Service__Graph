from enum import Enum


class Enum__Graph__Methods__Export(str, Enum):
    EXPORT_JSON       = "export_json"                           # Export to JSON format
    EXPORT_DOT        = "export_dot"                            # Export to DOT (Graphviz) format
    EXPORT_MERMAID    = "export_mermaid"                        # Export to Mermaid format
    SCREENSHOT        = "screenshot"                            # Generate image screenshot