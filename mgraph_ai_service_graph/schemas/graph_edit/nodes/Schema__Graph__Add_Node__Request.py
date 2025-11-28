from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Add_Node__Request(Type_Safe):
    graph_ref  : Schema__Graph__Ref         = None                              # Reference to target graph (or empty to create new)
    auto_cache : bool                       = True                              # Update cache after operation