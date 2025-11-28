from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                                      import Node_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe


class Schema__Graph__Neighbors__Request(Type_Safe):                                         # Request for neighbor queries
    graph_ref : Schema__Graph__Ref
    node_id   : Node_Id                                                                       # Node to get neighbors for
