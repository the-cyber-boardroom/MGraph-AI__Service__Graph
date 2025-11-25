from osbot_utils.type_safe.Type_Safe                                             import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                             import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid            import Random_Guid


class Schema__Graph__Create__Response(Type_Safe):
    graph_id   : Random_Guid                        # Generated ID
    node_count : Safe_UInt                          # Initial count (0)
    edge_count : Safe_UInt                          # Initial count (0)
    cached     : bool                               # Whether cached
    cache_id   : Random_Guid  = None                # Cache id (if cached in cache service)