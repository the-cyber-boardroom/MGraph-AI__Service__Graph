from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid


class Schema__Graph__Add_Node__Response(Type_Safe):
    node_id    : Obj_Id       = None
    graph_id   : Obj_Id       = None
    cache_id   : Random_Guid  = None
    cached     : bool         = False
    success    : bool         = False