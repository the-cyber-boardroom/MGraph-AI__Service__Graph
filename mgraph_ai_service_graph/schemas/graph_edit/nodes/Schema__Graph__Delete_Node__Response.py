from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Delete_Node__Response(Type_Safe):
    graph_ref : Schema__Graph__Ref          = None                              # Reference to parent graph
    node_id   : Obj_Id                      = None                              # Node that was deleted
    deleted   : bool                        = False                             # Whether deletion succeeded