from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class Schema__Graph__Find_Node__Request(Type_Safe):                                         # Request for single node lookup
    graph_id : Obj_Id                                                                       # Target graph
    node_id  : Obj_Id                                                                       # Node to find
