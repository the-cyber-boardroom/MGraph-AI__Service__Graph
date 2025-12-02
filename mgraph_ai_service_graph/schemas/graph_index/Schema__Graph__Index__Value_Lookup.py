from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.cryptography.safe_str.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id


class Schema__Graph__Index__Value_Lookup__Request(Type_Safe):                   # Request for value-based node lookup
    graph_ref  : Schema__Graph__Ref         = None                              # Reference to target graph
    value      : str                        = None                              # Value to search for
    value_type : str                        = 'str'                             # Type of the value (str, int, etc.)
    value_hash : Safe_Str__Cache_Hash       = None                              # Or lookup by hash directly
    key        : str                        = None                              # Optional key for value uniqueness
    from_cache : bool                       = True                              # Try to load from cached index first


class Schema__Graph__Index__Value_Lookup__Response(Type_Safe):                  # Response for value-based lookup
    graph_ref  : Schema__Graph__Ref         = None                              # Resolved reference
    node_id    : Node_Id                    = None                              # Found node ID (if exists)
    value      : str                        = None                              # The value searched for
    value_type : str                        = None                              # Type of the value
    value_hash : Safe_Str__Cache_Hash       = None                              # Hash of the value
    found      : bool                       = False                             # Whether value node was found
    from_cache : bool                       = False                             # Whether loaded from cache
    success    : bool                       = False                             # Whether operation succeeded
