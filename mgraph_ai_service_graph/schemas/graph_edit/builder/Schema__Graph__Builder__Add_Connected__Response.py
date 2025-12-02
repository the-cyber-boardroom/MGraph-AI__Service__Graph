from osbot_utils.type_safe.primitives.domains.identifiers.Edge_Id                          import Edge_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Builder__Add_Connected__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref          = None                              # Resolved reference
    node_id   : Node_Id                     = None                              # New node created
    edge_id   : Edge_Id                     = None                              # Edge connecting them
    cached    : bool                        = False                             # Whether changes were cached
    success   : bool                        = False                             # Whether operation succeeded