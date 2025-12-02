from typing                                                                     import Dict, Set, Tuple, Optional
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Index__Main(Type_Safe):                                    # Main index data structure
    # Node indexes
    nodes_by_type                   : Dict[str, Set[str]]                       # type_name -> set of node_ids
    nodes_types                     : Dict[str, str]                            # node_id -> type_name

    # Edge indexes
    edges_by_type                   : Dict[str, Set[str]]                       # type_name -> set of edge_ids
    edges_types                     : Dict[str, str]                            # edge_id -> type_name
    edges_to_nodes                  : Dict[str, Tuple[str, str]]                # edge_id -> (from_node_id, to_node_id)

    # Relationship indexes
    nodes_to_outgoing_edges         : Dict[str, Set[str]]                       # node_id -> set of edge_ids
    nodes_to_incoming_edges         : Dict[str, Set[str]]                       # node_id -> set of edge_ids
    nodes_to_outgoing_edges_by_type : Dict[str, Dict[str, Set[str]]]            # node_id -> {type: edge_ids}
    nodes_to_incoming_edges_by_type : Dict[str, Dict[str, Set[str]]]            # node_id -> {type: edge_ids}

    # Semantic indexes
    edges_predicates                : Dict[str, str]                            # edge_id -> predicate
    edges_by_predicate              : Dict[str, Set[str]]                       # predicate -> set of edge_ids
    edges_by_incoming_label         : Dict[str, Set[str]]                       # label -> set of edge_ids
    edges_by_outgoing_label         : Dict[str, Set[str]]                       # label -> set of edge_ids


class Schema__Graph__Index__Values(Type_Safe):                                  # Value index data structure
    hash_to_node   : Dict[str, str]                                             # value_hash -> node_id
    node_to_hash   : Dict[str, str]                                             # node_id -> value_hash
    values_by_type : Dict[str, Set[str]]                                        # type_name -> set of hashes
    type_by_value  : Dict[str, str]                                             # hash -> type_name


class Schema__Graph__Index__Full__Response(Type_Safe):                          # Response for full index retrieval
    graph_ref     : Schema__Graph__Ref              = None                      # Resolved reference
    main_index    : Schema__Graph__Index__Main      = None                      # Main index data
    values_index  : Schema__Graph__Index__Values    = None                      # Value index data (optional)
    from_cache    : bool                            = False                     # Whether loaded from cache
    success       : bool                            = False                     # Whether operation succeeded
