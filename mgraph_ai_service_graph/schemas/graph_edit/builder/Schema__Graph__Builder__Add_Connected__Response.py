from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id


class Schema__Graph__Builder__Add_Connected__Response(Type_Safe):
    node_id        : Obj_Id       = None                                # New node created
    edge_id        : Obj_Id       = None                                # Edge connecting them
    graph_id       : Obj_Id       = None
    cache_id       : str          = None
    cached         : bool         = False
    success        : bool         = False