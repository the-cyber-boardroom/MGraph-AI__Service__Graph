from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid           import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id


class Schema__Graph__Find_Nodes__Request(Type_Safe):
    cache_id   : Random_Guid        = None
    graph_id   : Obj_Id             = None          # Target graph
    node_type  : Safe_Str__Id       = None          # Type to search        # todo: check if this shouldn't be a Type[Node_Type]
    limit      : Safe_UInt          = 100           # Max results
    offset     : Safe_UInt          = 0             # Pagination

