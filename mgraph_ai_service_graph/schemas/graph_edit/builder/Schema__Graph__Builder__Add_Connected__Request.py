from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id


class Schema__Graph__Builder__Add_Connected__Request(Type_Safe):
    graph_id       : Obj_Id          = None
    namespace      : Safe_Str__Id    = None
    from_node_id   : Obj_Id          = None                             # Starting node
    value          : str             = None                             # Value for new connected node
    predicate      : str             = None                             # Optional predicate
    auto_cache     : bool            = True