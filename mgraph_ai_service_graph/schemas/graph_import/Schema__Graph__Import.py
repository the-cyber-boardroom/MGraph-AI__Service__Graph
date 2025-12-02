from typing                                                                     import Dict, Any
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Import__Request(Type_Safe):                                # Request for importing a full graph
    graph_data   : Dict[str, Any]       = None                                  # Full graph JSON data (standard format)
    namespace    : Safe_Str__Id         = 'graph-service'                       # Namespace for the imported graph
    auto_cache   : bool                 = True                                  # Cache after import
    build_index  : bool                 = True                                  # Build and cache index after import
    validate     : bool                 = True                                  # Validate graph structure before import


class Schema__Graph__Import__Compressed__Request(Type_Safe):                    # Request for importing compressed graph format
    graph_data   : Dict[str, Any]       = None                                  # Compressed graph JSON data
    namespace    : Safe_Str__Id         = 'graph-service'                       # Namespace for the imported graph
    auto_cache   : bool                 = True                                  # Cache after import
    build_index  : bool                 = True                                  # Build and cache index after import


class Schema__Graph__Import__Response(Type_Safe):                               # Response for graph import
    graph_ref     : Schema__Graph__Ref      = None                              # Reference to imported graph
    nodes_count   : Safe_UInt                                                   # Number of nodes imported
    edges_count   : Safe_UInt                                                   # Number of edges imported
    index_cached  : bool                    = False                             # Whether index was cached
    cached        : bool                    = False                             # Whether graph was cached
    success       : bool                    = False                             # Whether import succeeded
    validation_errors: list                                                     # Any validation errors encountered
