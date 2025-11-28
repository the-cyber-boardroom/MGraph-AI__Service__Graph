from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                           import Schema__Graph__Ref
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id


class Schema__Graph__Find_Edges__Request(Type_Safe):                                        # Request for edge type queries
    graph_ref : Schema__Graph__Ref
    edge_type : Safe_Str__Id                                                                # Type of edges to find
