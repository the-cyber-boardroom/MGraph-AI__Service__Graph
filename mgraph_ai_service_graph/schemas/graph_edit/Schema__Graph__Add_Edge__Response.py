from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.Random_Guid                       import Random_Guid


class Schema__Graph__Add_Edge__Response(Type_Safe):                                         # Response for edge addition operations
    edge_id      : Obj_Id       = None                                                      # Created edge ID
    graph_id     : Obj_Id       = None                                                      # Parent graph
    from_node_id : Obj_Id       = None                                                      # Source node of edge
    to_node_id   : Obj_Id       = None                                                      # Target node of edge
    cache_id     : Random_Guid  = None                                                      # Cache ID if cached
    cached       : bool         = False                                                     # Whether cached
    success      : bool         = False                                                     # Whether operation succeeded