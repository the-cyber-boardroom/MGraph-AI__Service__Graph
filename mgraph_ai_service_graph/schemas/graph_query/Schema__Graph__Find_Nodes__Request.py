from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Find_Nodes__Request(Type_Safe):
    graph_ref  : Schema__Graph__Ref         = None                              # Reference to target graph
    node_type  : Safe_Str__Id               = None                              # Type to search
    limit      : Safe_UInt                  = 100                               # Max results
    offset     : Safe_UInt                  = 0                                 # Pagination offset