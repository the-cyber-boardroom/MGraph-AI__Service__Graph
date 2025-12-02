from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Cache_Id              import Cache_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Graph_Id              import Graph_Id


GRAPH_REF__DEFAULT_NAMESPACE = 'graph-service'

class Schema__Graph__Ref(Type_Safe):                                                 # Canonical reference to identify a graph
    cache_id  : Cache_Id             = ''                                            # Direct cache lookup (most efficient)
    graph_id  : Graph_Id             = ''                                            # Lookup by graph's internal ID
    namespace : Safe_Str__Id  = GRAPH_REF__DEFAULT_NAMESPACE                  # Required context for cache operations