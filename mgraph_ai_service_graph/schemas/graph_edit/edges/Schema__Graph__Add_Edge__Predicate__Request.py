from mgraph_ai_service_graph.schemas.graph_ref.Node_Id                          import Node_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Add_Edge__Predicate__Request(Type_Safe):
    graph_ref    : Schema__Graph__Ref       = None                              # Reference to target graph
    from_node_id : Node_Id                   = None                              # Source node
    to_node_id   : Node_Id                   = None                              # Target node
    predicate    : Safe_Str__Id             = None                              # Semantic relationship name
    auto_cache   : bool                     = True                              # Update cache after operation