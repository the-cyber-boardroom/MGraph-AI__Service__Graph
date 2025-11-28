from enum import Enum

class Enum__Graph__Methods__CRUD(str, Enum):                     # Methods for graph CRUD operations
    CREATE_GRAPH = "create_graph"                                # Create new empty graph
    GET_GRAPH    = "get_graph"                                   # Retrieve graph by ID
    DELETE_GRAPH = "delete_graph"                                # Delete graph from cache
    LIST_GRAPHS  = "list_graphs"                                 # List all cached graphs
    GRAPH_EXISTS = "graph_exists"                                # Check if graph exists
    GRAPH_STATS  = "graph_stats"                                 # Get graph statistics