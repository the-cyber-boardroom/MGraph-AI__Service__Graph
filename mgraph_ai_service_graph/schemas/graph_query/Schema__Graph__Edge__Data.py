from typing                                                                                 import Dict
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text


class Schema__Graph__Edge__Data(Type_Safe):                                                 # Edge data structure for query results
    edge_id      : Obj_Id                                                                   # Edge identifier
    from_node_id : Obj_Id                                                                   # Source node
    to_node_id   : Obj_Id                                                                   # Target node
    edge_type    : Safe_Str__Id                                                             # Edge type/relationship
    edge_data    : Dict[Safe_Str__Key, Safe_Str__Text]                                      # Edge attributes
