from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id
from osbot_utils.type_safe.primitives.domains.identifiers.safe_str.Safe_Str__Id             import Safe_Str__Id


class Schema__Graph__Find_Edges__Request(Type_Safe):                                        # Request for edge type queries
    graph_id  : Obj_Id                                                                      # Target graph
    edge_type : Safe_Str__Id                                                                # Type of edges to find
