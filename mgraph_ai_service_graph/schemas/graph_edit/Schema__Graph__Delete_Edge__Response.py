from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class Schema__Graph__Delete_Edge__Response(Type_Safe):                                      # Response for edge deletion operations
    graph_id : Obj_Id                                                                       # Parent graph
    edge_id  : Obj_Id                                                                       # Edge that was deleted
    deleted  : bool             = False                                                     # Whether deletion succeeded
