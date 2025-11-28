from typing                                                                         import Dict
from osbot_utils.type_safe.Type_Safe                                                import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                    import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id     import Safe_Str__Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Key    import Safe_Str__Key
from osbot_utils.type_safe.primitives.domains.common.safe_str.Safe_Str__Text        import Safe_Str__Text
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref                   import Schema__Graph__Ref


class Schema__Graph__Find_Node__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref                      = None                  # Resolved reference
    node_id   : Obj_Id                                  = None                  # Found node ID
    node_type : Safe_Str__Id                            = None                  # Node type name
    node_data : Dict[Safe_Str__Key, Safe_Str__Text]     = None                  # Node properties
    found     : bool                                    = False                 # Whether node was found