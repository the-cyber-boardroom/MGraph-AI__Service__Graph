from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Index__ReIndex__Request(Type_Safe):                        # Request for re-indexing
    graph_ref    : Schema__Graph__Ref   = None                                  # Reference to target graph
    cache_index  : bool                 = True                                  # Cache the newly built index


class Schema__Graph__Index__ReIndex__Response(Type_Safe):                       # Response for re-indexing
    graph_ref        : Schema__Graph__Ref   = None                              # Resolved reference
    nodes_indexed    : Safe_UInt                                                # Number of nodes indexed
    edges_indexed    : Safe_UInt                                                # Number of edges indexed
    values_indexed   : Safe_UInt                                                # Number of value nodes indexed
    predicates_found : Safe_UInt                                                # Number of predicates found
    index_cached     : bool                 = False                             # Whether index was cached
    success          : bool                 = False                             # Whether operation succeeded
