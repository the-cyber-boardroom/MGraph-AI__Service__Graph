from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id


class Schema__Graph__Add_Node__Request(Type_Safe):              # Basic node addition
    graph_id   : Obj_Id          = None
    cache_id   : Random_Guid     = None
    namespace  : Safe_Str__Id    = None
    auto_cache : bool            = True                                       # Update cache after operation
