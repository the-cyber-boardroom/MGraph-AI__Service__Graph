from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Obj_Id                import Obj_Id
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Add_Edge__Request(Type_Safe):
    graph_ref    : Schema__Graph__Ref       = None                              # Reference to target graph
    from_node_id : Obj_Id                   = None                              # Source node
    to_node_id   : Obj_Id                   = None                              # Target node
    auto_cache   : bool                     = True                              # Update cache after operation