from typing                                                                     import List
from osbot_utils.type_safe.primitives.domains.identifiers.Node_Id                          import Node_Id
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Find_Nodes__Response(Type_Safe):
    graph_ref   : Schema__Graph__Ref        = None                              # Resolved reference
    node_ids    : List[Node_Id]                                                 # Found node IDs
    total_found : Safe_UInt                                                     # Total matches
    has_more    : bool                      = False                             # More results available