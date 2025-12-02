from typing                                                                     import Dict
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Index__Stats__Request(Type_Safe):                          # Request for index statistics
    graph_ref  : Schema__Graph__Ref     = None                                  # Reference to target graph
    from_cache : bool                   = True                                  # Try to load from cached index first


class Schema__Graph__Index__Stats__Response(Type_Safe):                         # Response for index statistics
    graph_ref               : Schema__Graph__Ref        = None                  # Resolved reference

    # Node statistics
    total_nodes             : Safe_UInt                                         # Total number of nodes
    node_types_count        : Safe_UInt                                         # Number of distinct node types
    nodes_by_type_counts    : Dict[str, int]                                    # Count per node type

    # Edge statistics
    total_edges             : Safe_UInt                                         # Total number of edges
    edge_types_count        : Safe_UInt                                         # Number of distinct edge types
    edges_by_type_counts    : Dict[str, int]                                    # Count per edge type

    # Predicate statistics
    total_predicates        : Safe_UInt                                         # Total unique predicates
    edges_by_predicate_counts: Dict[str, int]                                   # Count per predicate

    # Value node statistics
    total_value_nodes       : Safe_UInt                                         # Total value nodes
    value_types_count       : Safe_UInt                                         # Number of distinct value types
    values_by_type_counts   : Dict[str, int]                                    # Count per value type

    # Index metadata
    index_cached            : bool                      = False                 # Whether index is cached
    from_cache              : bool                      = False                 # Whether loaded from cache
    success                 : bool                      = False                 # Whether operation succeeded
