from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text
from typing                                                                                 import Dict


class Schema__Graph__Add_Edge__Request(Type_Safe):
    graph_id     : Obj_Id                                                                   # Target graph
    from_node_id : Obj_Id                                                                   # Source node
    to_node_id   : Obj_Id                                                                   # Target node
    edge_type    : Safe_Str__Id                                                             # Edge type/relationship
    edge_data    : Dict[Safe_Str__Key, Safe_Str__Text]                                      # Edge attributes (type-safe)
    auto_cache   : bool                    = True                                           # Update cache after operation
