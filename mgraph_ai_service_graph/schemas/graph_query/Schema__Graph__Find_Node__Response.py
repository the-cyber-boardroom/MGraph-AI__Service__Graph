from typing                                                                                 import Dict
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key            import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text                import Safe_Str__Text


class Schema__Graph__Find_Node__Response(Type_Safe):                                        # Response for single node lookup
    graph_id  : Obj_Id                                                                      # Parent graph
    node_id   : Obj_Id                                                                      # Found node ID
    node_type : Safe_Str__Id                                                                # Node type name
    node_data : Dict[Safe_Str__Key, Safe_Str__Text]                                         # Node properties
    found     : bool            = False                                                     # Whether node was found
