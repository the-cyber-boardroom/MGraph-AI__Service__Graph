from enum import Enum


class Enum__Graph__Methods__Export(str, Enum):
    EXPORT_JSON     = "export_json"
    EXPORT_DOT      = "export_dot"
    EXPORT_MERMAID  = "export_mermaid"
    IMPORT_JSON     = "import_json"
    IMPORT_DOT      = "import_dot"
    IMPORT_MERMAID  = "import_mermaid"