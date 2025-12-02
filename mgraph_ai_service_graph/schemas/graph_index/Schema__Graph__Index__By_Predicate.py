from typing                                                                     import List
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                          import Edge_Id


class Schema__Graph__Index__By_Predicate__Request(Type_Safe):                   # Request for predicate-based node lookup
    graph_ref    : Schema__Graph__Ref       = None                              # Reference to target graph
    from_node_id : Node_Id                  = None                              # Starting node (optional)
    predicate    : Safe_Str__Id             = None                              # Predicate to search for
    direction    : str                      = 'outgoing'                        # 'incoming' or 'outgoing'
    from_cache   : bool                     = True                              # Try to load from cached index first


class Schema__Graph__Index__By_Predicate__Response(Type_Safe):                  # Response for predicate-based lookup
    graph_ref      : Schema__Graph__Ref     = None                              # Resolved reference
    predicate      : Safe_Str__Id           = None                              # Queried predicate
    from_node_id   : Node_Id                = None                              # Starting node (if provided)
    target_node_ids: List[Node_Id]                                              # Nodes connected via predicate
    edge_ids       : List[Edge_Id]                                              # Edges with this predicate
    total_found    : Safe_UInt                                                  # Total matches
    from_cache     : bool                   = False                             # Whether loaded from cache
    success        : bool                   = False                             # Whether operation succeeded
