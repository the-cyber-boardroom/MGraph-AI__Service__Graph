from mgraph_ai_service_graph.schemas.graph_ref.Edge_Id                          import Edge_Id
from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                          import Node_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Add_Edge__Response(Type_Safe):
    graph_ref    : Schema__Graph__Ref       = None                              # Resolved reference
    edge_id      : Edge_Id                  = None                              # Created edge ID
    from_node_id : Node_Id                  = None                              # Source node
    to_node_id   : Node_Id                  = None                              # Target node
    cached       : bool                     = False                             # Whether changes were cached
    success      : bool                     = False                             # Whether operation succeeded