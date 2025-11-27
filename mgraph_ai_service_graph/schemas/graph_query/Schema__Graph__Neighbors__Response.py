from typing                                                                                 import List
from osbot_utils.type_safe.Type_Safe                                                        import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                            import Obj_Id


class Schema__Graph__Neighbors__Response(Type_Safe):                                        # Response for neighbor queries
    graph_id     : Obj_Id                                                                   # Source graph
    node_id      : Obj_Id                                                                   # Node whose neighbors were queried
    neighbor_ids : List[Obj_Id]                                                             # List of neighbor node IDs
    total_found  : Safe_UInt                                                                # Total neighbors found
