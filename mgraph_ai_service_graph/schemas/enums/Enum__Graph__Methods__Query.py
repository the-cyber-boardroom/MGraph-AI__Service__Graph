from enum import Enum


class Enum__Graph__Methods__Query(str, Enum):
    FIND_NODE           = "find_node"
    FIND_NODES_BY_TYPE  = "find_nodes_by_type"
    FIND_EDGES_BY_TYPE  = "find_edges_by_type"
    GET_NEIGHBORS       = "get_neighbors"
    GET_NODE_PATH       = "get_node_path"
    QUERY_BY_PREDICATE  = "query_by_predicate"
    SEARCH_VALUE_NODES  = "search_value_nodes"