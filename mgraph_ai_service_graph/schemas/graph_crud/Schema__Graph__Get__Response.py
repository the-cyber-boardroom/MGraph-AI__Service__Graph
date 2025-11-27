from mgraph_db.mgraph.MGraph import MGraph
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid


class Schema__Graph__Get__Response(Type_Safe):
    graph_id   : Obj_Id                                                                 # Retrieved graph ID
    #cached     : bool                                                                  # Whether graph is cached
    cache_id   : Random_Guid           = None                                           # Cache ID if cached
    mgraph     : MGraph
    success    : bool
