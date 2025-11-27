from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class Schema__Graph__Neighbors__Request(Type_Safe):                                         # Request for neighbor queries
    graph_id : Obj_Id                                                                       # Target graph
    node_id  : Obj_Id                                                                       # Node to get neighbors for
