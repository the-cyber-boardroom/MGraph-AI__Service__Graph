from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Index__Request(Type_Safe):                                 # Base request for index operations
    graph_ref  : Schema__Graph__Ref     = None                                  # Reference to target graph
    from_cache : bool                   = True                                  # Try to load from cached index first


class Schema__Graph__Index__Full__Request(Schema__Graph__Index__Request):       # Request for full index retrieval
    include_values : bool               = True                                  # Include value index in response
