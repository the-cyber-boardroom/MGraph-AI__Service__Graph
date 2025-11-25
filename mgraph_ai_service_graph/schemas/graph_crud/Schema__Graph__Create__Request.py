from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Display_Name   import Safe_Str__Display_Name
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Namespace      import Safe_Str__Namespace


class Schema__Graph__Create__Request(Type_Safe):
    graph_name : Safe_Str__Display_Name = None     # Optional name
    auto_cache : bool                   = True      # Auto-cache after creation
    namespace  : Safe_Str__Namespace    = "default" # Cache namespace
