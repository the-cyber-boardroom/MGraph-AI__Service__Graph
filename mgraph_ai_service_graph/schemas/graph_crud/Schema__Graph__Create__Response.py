from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                 import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid            import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id  import Safe_Str__Id


class Schema__Graph__Create__Response(Type_Safe):
    graph_id        : Obj_Id                        # Generated ID
    cached          : bool                          # Whether cached
    cache_id        : Random_Guid         = None    # Cache id (if cached in cache service)
    cache_namespace : Safe_Str__Id        = None    # Cache namespace (this is needed in order to get the graph_id) # todo: see if we should not just use 'namespace' here, instead of 'cache_namespace'