from typing                                                                     import List, Set
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                          import Edge_Id


class Schema__Graph__Index__Node_Edges__Request(Type_Safe):                     # Request for node edge lookup
    graph_ref  : Schema__Graph__Ref     = None                                  # Reference to target graph
    node_id    : Node_Id                = None                                  # Node to get edges for
    direction  : str                    = 'both'                                # 'incoming', 'outgoing', or 'both'
    edge_type  : str                    = None                                  # Optional filter by edge type
    from_cache : bool                   = True                                  # Try to load from cached index first


class Schema__Graph__Index__Node_Edges__Response(Type_Safe):                    # Response for node edge lookup
    graph_ref       : Schema__Graph__Ref        = None                          # Resolved reference
    node_id         : Node_Id                   = None                          # Queried node
    incoming_edges  : List[Edge_Id]                                             # Edge IDs for incoming edges
    outgoing_edges  : List[Edge_Id]                                             # Edge IDs for outgoing edges
    incoming_count  : Safe_UInt                                                 # Count of incoming edges
    outgoing_count  : Safe_UInt                                                 # Count of outgoing edges
    from_cache      : bool                      = False                         # Whether loaded from cache
    success         : bool                      = False                         # Whether operation succeeded
