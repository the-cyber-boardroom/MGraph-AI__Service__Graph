from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                              import Node_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                                  import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                   import Schema__Graph__Ref


class Schema__Graph__Find_Node__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref                      = None                  # Resolved reference
    node_id   : Node_Id                                 = None                  # Found node ID
    node_data : Schema__MGraph__Node                    = None                  # Node object
    found     : bool                                    = False                 # Whether node was found