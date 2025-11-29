from typing                                                                     import Type
from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                          import Node_Id
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                              import Schema__MGraph__Edge
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Add_Edge__Typed__Request(Type_Safe):
    graph_ref    : Schema__Graph__Ref               = None                      # Reference to target graph
    from_node_id : Node_Id                          = None                      # Source node
    to_node_id   : Node_Id                          = None                      # Target node
    edge_type    : Type[Schema__MGraph__Edge]       = None                      # Edge type class
    auto_cache   : bool                             = True                      # Update cache after operation