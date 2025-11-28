from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id

# todo: refactor default namespace below
class Schema__Graph__Get__Request(Type_Safe):
    cache_id  : Random_Guid     = None                                               # Graph cache_id
    graph_id  : Obj_Id          = None                                               # Graph to retrieve
    namespace : Safe_Str__Id    = None                                               # Cache namespace
