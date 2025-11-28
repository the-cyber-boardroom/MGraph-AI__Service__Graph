from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Display_Name   import Safe_Str__Display_Name
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref


class Schema__Graph__Create__Request(Type_Safe):
    graph_ref  : Schema__Graph__Ref         = None                              # Optional - if provided with cache_id/graph_id, will be ignored (create always makes new)
    graph_name : Safe_Str__Display_Name     = None                              # Optional name
    auto_cache : bool                       = True                              # Auto-cache after creation