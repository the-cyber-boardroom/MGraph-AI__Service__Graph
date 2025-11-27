from typing                                                                                 import List
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id
from mgraph_ai_service_graph.schemas.graph_query.Schema__Graph__Edge__Data                  import Schema__Graph__Edge__Data


class Schema__Graph__Find_Edges__Response(Type_Safe):                                       # Response for edge type queries
    graph_id    : Obj_Id                                                                    # Source graph
    edge_type   : Safe_Str__Id                                                              # Edge type that was queried
    edges       : List[Schema__Graph__Edge__Data]                                           # Found edges
    total_found : Safe_UInt                                                                 # Total matches
