from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid


class Schema__Graph__Add_Node__Response(Type_Safe):                                         # Response for node addition operations
    node_id  : Obj_Id       = None                                                          # Created node ID
    graph_id : Obj_Id       = None                                                          # Parent graph
    cache_id : Random_Guid  = None                                                          # Cache ID if cached
    cached   : bool         = False                                                         # Whether cached
    success  : bool         = False                                                         # Whether operation succeeded