from typing                                                                                 import Dict
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text


class Schema__Graph__Add_Node__Request(Type_Safe):
    graph_id   : Obj_Id         = None                                                            # Target graph
    graph_cache: Random_Guid    = None
    namespace : Safe_Str__Id    = None
    node_type  : Safe_Str__Id                                                               # Node type name
    node_data  : Dict[Safe_Str__Key, Safe_Str__Text]                                        # Node properties (type-safe dict)
    auto_cache : bool                      = True                                           # Update cache after operation
