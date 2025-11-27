from typing                                                                     import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Edge                              import Schema__MGraph__Edge
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid           import Random_Guid
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id import Safe_Str__Id


class Schema__Graph__Add_Edge__Typed__Request(Type_Safe):       # Typed edge addition
    graph_id     : Obj_Id                       = None
    cache_id     : Random_Guid                  = None
    namespace    : Safe_Str__Id                 = None
    from_node_id : Obj_Id                       = None
    to_node_id   : Obj_Id                       = None
    edge_type    : Type[Schema__MGraph__Edge]   = None
    auto_cache   : bool                         = True
