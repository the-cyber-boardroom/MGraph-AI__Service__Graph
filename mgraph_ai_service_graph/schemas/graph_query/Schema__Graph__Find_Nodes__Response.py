from typing                                                             import List
from osbot_utils.type_safe.Type_Safe                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id        import Obj_Id


class Schema__Graph__Find_Nodes__Response(Type_Safe):
    graph_id   : Obj_Id                            # Source graph
    node_ids   : List[Obj_Id]                       # Found node IDs
    total_found: Safe_UInt                          # Total matches
    has_more   : bool                               # More results available