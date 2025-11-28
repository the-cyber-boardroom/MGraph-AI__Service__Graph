from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from mgraph_ai_service_cache_client.schemas.cache.Cache_Id                      import Cache_Id

GRAPH_REF__DEFAULT_NAMESPACE = 'graph-service'

# todo: replace the use of Obj_Id below with a new class called Graph_Id (created in a way to allow Null and Empty values, just like what we will de doing with Cache_Id
class Schema__Graph__Ref(Type_Safe):                                            # Canonical reference to identify a graph
    cache_id  : Cache_Id        = None                                          # Direct cache lookup (most efficient)
    graph_id  : Obj_Id          = None                                          # Lookup by graph's internal ID
    namespace : Safe_Str__Id    = GRAPH_REF__DEFAULT_NAMESPACE                  # Required context for cache operations