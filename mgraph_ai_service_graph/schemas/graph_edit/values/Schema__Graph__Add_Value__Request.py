from typing                                                                     import Type
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid           import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id


class Schema__Graph__Add_Value__Request(Type_Safe):             # Value node addition
    graph_id   : Obj_Id          = None
    cache_id   : Random_Guid     = None
    namespace  : Safe_Str__Id    = None
    value      : str             = None                         # The value to store
    key        : str             = None                         # Optional key for uniqueness
    #value_type : Type            = str                          # Python type of value         # todo: see how we can add more types than string (and if we need that)
    auto_cache : bool            = True
