from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                          import Node_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Builder__Add_Connected__Request(Type_Safe):
    graph_ref      : Schema__Graph__Ref     = None                              # Reference to target graph
    from_node_id   : Node_Id                 = None                              # Starting node
    value          : str                    = None                              # Value for new connected node
    predicate      : str                    = None                              # Optional predicate
    auto_cache     : bool                   = True                              # Update cache after operation