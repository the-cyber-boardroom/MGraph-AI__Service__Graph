from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class Schema__Graph__Add_Edge__Response(Type_Safe):
    edge_id  : Obj_Id                                                                       # Created edge ID
    graph_id : Obj_Id                                                                       # Parent graph
    cached   : bool                                                                         # Whether cached
