from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Add_Value__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref          = None                              # Resolved reference
    node_id   : Obj_Id                      = None                              # Created/found value node ID
    value     : str                         = None                              # The stored value
    cached    : bool                        = False                             # Whether changes were cached
    success   : bool                        = False                             # Whether operation succeeded