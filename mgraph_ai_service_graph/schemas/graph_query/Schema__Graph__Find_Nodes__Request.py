from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id


class Schema__Graph__Find_Nodes__Request(Type_Safe):
    graph_id   : Obj_Id                             # Target graph
    node_type  : Safe_Str__Id                       # Type to search
    limit      : Safe_UInt          = 100           # Max results
    offset     : Safe_UInt          = 0             # Pagination

