from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id


class Schema__Graph__Exists__Response(Type_Safe):                                           # Response for graph existence check
    graph_id  : Obj_Id          = None                                                      # Graph that was checked
    cache_id  : Random_Guid     = None                                                      # Cache ID if applicable
    namespace : Safe_Str__Id    = None                                                      # Cache namespace
    exists    : bool            = False                                                     # Whether graph exists
