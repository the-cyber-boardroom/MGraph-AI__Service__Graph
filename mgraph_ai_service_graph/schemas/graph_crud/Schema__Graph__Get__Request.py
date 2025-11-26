from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id

# todo: refactor default namespace below
class Schema__Graph__Get__Request(Type_Safe):
    graph_id  : Obj_Id                                                                 # Graph to retrieve
    namespace : Safe_Str__Id    = "default"                                            # Cache namespace
