from typing                                                                     import Type
from mgraph_db.mgraph.schemas.Schema__MGraph__Node__Data                        import Schema__MGraph__Node__Data
from mgraph_db.mgraph.schemas.Schema__MGraph__Node                              import Schema__MGraph__Node
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from mgraph_ai_service_graph.schemas.graph_ref.Schema__Graph__Ref               import Schema__Graph__Ref


class Schema__Graph__Add_Node__Typed__Request(Type_Safe):
    graph_ref  : Schema__Graph__Ref                     = None                  # Reference to target graph
    node_type  : Type[Schema__MGraph__Node]             = None                  # Node type class
    node_data  : Schema__MGraph__Node__Data             = None                  # Node data
    auto_cache : bool                                   = True                  # Update cache after operation