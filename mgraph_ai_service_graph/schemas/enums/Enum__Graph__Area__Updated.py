from enum import Enum

class Enum__Graph__Area(str, Enum):                              # Functional areas for graph service operations
    GRAPH_CRUD   = "graph_crud"                                  # Create, Read, Update, Delete graphs
    GRAPH_EDIT   = "graph_edit"                                  # Add/remove nodes/edges
    GRAPH_QUERY  = "graph_query"                                 # Search and exploration
    GRAPH_CACHE  = "graph_cache"                                 # Cache operations
    GRAPH_EXPORT = "graph_export"                                # Format conversion (JSON, DOT, Mermaid)
    GRAPH_INDEX  = "graph_index"                                 # NEW: Index operations
    GRAPH_IMPORT = "graph_import"                                # NEW: Graph import operations
