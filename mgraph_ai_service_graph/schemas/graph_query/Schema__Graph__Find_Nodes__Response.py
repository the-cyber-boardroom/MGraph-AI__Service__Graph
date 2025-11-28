from typing                                                                     import List
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Find_Nodes__Response(Type_Safe):
    graph_ref   : Schema__Graph__Ref        = None                              # Resolved reference
    node_ids    : List[Obj_Id]              = None                              # Found node IDs
    total_found : Safe_UInt                 = None                              # Total matches
    has_more    : bool                      = False                             # More results available